from datetime import datetime
import os

from flask import (
    abort, 
    Flask, 
    jsonify, 
    render_template, 
    request, 
    send_from_directory
)
from flask.ext.mongoengine import MongoEngine
from goosepaper import app
from goosepaper.helpers import extract, save_article
from goosepaper.models import SavedArticle


@app.route('/favorites', methods=['POST', 'DELETE', 'GET'])
def favorites(id=None):
    """ Manage favorites """
    if request.method == 'GET':
        return render_template('favorites.html', articles=SavedArticle.objects(favorite=True).order_by('-sent'))

    # Get the ID. Abort if not supplied in headers.
    if 'Id' not in request.headers:
        abort(401)
    id = request.headers['Id'].strip()

    # Set or unset the favorites attribute depending on request method
    action = {'POST': True, 'DELETE': False}
    SavedArticle.objects.get_or_404(id__exact=id).update(set__favorite=action[request.method])
    return "OK\n"


@app.route('/save')
def save():
    print str(request.params)
    return str(request.params)


@app.route('/articles/<id>', methods=['GET', 'DELETE'])
def article(id=None):
    """ Display or remove a single saved article """
    article = SavedArticle.objects.get_or_404(id__exact=id)

    # Display or delete the article depending on request method
    if request.method in ['GET', 'get']:
        return render_template('article.html', article=article)
    elif request.method in ['DELETE', 'delete']:
        try:
            article.delete()
        except Exception, e:
            abort(500)
    return "Removed"


@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
@app.route('/articles')
def index():
    """ Save a URI or show some information on how to do so """
    # Display articles if GET-ting a page
    if request.method == 'GET':
        return render_template("index.html", 
                               articles=SavedArticle.objects().order_by('-sent'))

    # Only other method allowed at this point is POST. 
    # Check for 'Article' header and get the URL.
    if 'Article' not in request.headers:
        abort(401)
    url = request.headers['Article'].strip()

    # Attempt to extract and save article
    article = extract(url)
    if not save_article(article):
        abort(400)

    return jsonify({})


@app.route('/favicon.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.png')

