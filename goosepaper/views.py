from datetime import datetime
import os

from flask import Flask, render_template, request, abort, jsonify, send_from_directory
from flask.ext.mongoengine import MongoEngine
from mongoengine.errors import ValidationError
from goosepaper import app
from goosepaper.models import Article
from goosepaper.helpers import extract, save_article


@app.route('/articles/<id>', methods=['GET', 'DELETE'])
def article(id=None):
    """ Display or remove a single saved article """
    article = Article.objects.get_or_404(id__exact=id)

    # Display or delete the article depending on request method
    if request.method in ['GET', 'get']:
        return render_template('article.html', article=article)
    elif request.method in ['DELETE', 'delete']:
        try:
            article.delete()
        except Exception, e:
            abort(500)
    return "Removed\n"


@app.route('/save', methods=['GET', 'POST'])
def save():
    """ Save a URI or show some information on how to do so """
    # Display information if GET-ting page
    if request.method == 'GET':
        return render_template('save.html')

    # Only other method allowed at this point is POST. 
    # Check for 'Article' header
    if 'Article' not in request.headers:
        abort(401)

    url = request.headers['Article'].strip()

    # Check if document exists
    if Article.objects(url__exact=url):
        return "Exists\n"

    article = extract(url)
    save_article(article)
    return "OK\n"


@app.route('/')
@app.route('/index')
@app.route('/articles')
def index():
    return render_template("index.html", 
                           articles=Article.objects().order_by('-sent'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

