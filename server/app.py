#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    articles = [article.to_dict() for article in Article.query.all()]
    resp = articles

    return resp

@app.route('/articles/<int:id>')
def show_article(id):

# Initialize session['page_views'] to 0 if it's the user's first request
    session['page_views'] = session.get('page_views', 0)
# Increment the page_views count for every request
    session['page_views'] += 1

    # Check if the user has viewed more than 3 pages
    if session['page_views'] <= 3:
        # Return article data if the limit has not been reached
        article = Article.query.filter(Article.id == id).first().to_dict()
        return article
    else:
        resp_body = {'message': 'Maximum pageview limit reached'}
        resp = make_response(resp_body, 401)
        return resp

if __name__ == '__main__':
    app.run(port=5555)
