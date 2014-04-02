from datetime import datetime
import os

from flask import Flask, render_template, request, abort, jsonify, send_from_directory
from goose import Goose

from mongoengine.errors import ValidationError
from things_i_read import app
from things_i_read.models import Article
from flask.ext.mongoengine import MongoEngine


def extract(url=None):
    """ Attempts to extract article from URL """
    g = Goose()
    try:
        article = g.extract(url=url)
    except ValidationError, e:
        return "Oh poop...", str(e)

    article.url = url
    return article


def save_article(article):
    """ Save article to MongoDB instance """
    if article.title:
        Article( title=article.title,
                 sent=str(datetime.now()),
                 url=article.url,
                 body=article.cleaned_text,
                 domain=article.domain.replace('www.',''),
                 summary=article.cleaned_text[:255] ).save()


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

