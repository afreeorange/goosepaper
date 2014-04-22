from datetime import datetime
import os
import json

from flask import (
    abort, 
    Flask, 
    jsonify, 
    render_template, 
    request, 
    Response,
    send_from_directory
)
from mongoengine import Q
from flask.ext.mongoengine import MongoEngine, Pagination
from goosepaper import app
from goosepaper.helpers import extract, save_article, mongo_object_to_dict
from goosepaper.models import SavedArticle


@app.route('/favorites/page/<int:number>')
@app.route('/favorites/page')
@app.route('/favorites', methods=['POST', 'DELETE', 'GET'])
def favorites(number=1):
    """ Manage favorites """
    if request.method == 'GET':
        paginator = Pagination(SavedArticle.objects(favorite=True).order_by('-sent'), number, app.config['ARTICLES_PER_PAGE'])
        return render_template('favorites.html', paginator=paginator)

    # Get the ID. Abort if not supplied in headers.
    if 'Id' not in request.headers:
        abort(401)
    id = request.headers['Id'].strip()

    # Set or unset the favorites attribute depending on request method
    action = {'POST': True, 'DELETE': False}
    SavedArticle.objects.get_or_404(id__exact=id).update(set__favorite=action[request.method])
    return "OK\n"


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


@app.route('/search/<string:term>/page/<int:number>')
@app.route('/search/<string:term>')
def search(term, number=1):
    term = term.strip()

    if len(term) < 4:
        return jsonify({'error': 'Search term must be longer than 3 characters'})

    paginator = Pagination(SavedArticle.objects(Q(title__icontains=term) | Q(domain__icontains=term) | Q(body__icontains=term)).exclude('body').order_by('-sent'), number, app.config['ARTICLES_PER_PAGE'])
    return render_template("index.html", paginator=paginator, term=term)

    # results = []
    # for article in articles:
    #     results.append(mongo_object_to_dict(article))

    # http://flask.pocoo.org/docs/security/#json-security
    # return Response(json.dumps(results), mimetype='application/json')


@app.route('/page/<int:number>')
@app.route('/articles')
@app.route('/index')
@app.route('/', methods=['GET', 'POST'])
def index(number=1):
    """ Save a URI or show some information on how to do so """
    # Display articles if GET-ting a page
    if request.method == 'GET':
        paginator = Pagination(SavedArticle.objects.order_by('-sent'), number, app.config['ARTICLES_PER_PAGE'])
        return render_template("index.html", paginator=paginator)

    # Only other method allowed at this point is POST. 
    # Check for 'Article' header and get the URL.
    if 'Article' not in request.headers:
        abort(401)
    url = request.headers['Article'].strip()

    # Attempt to extract and save article
    article = extract(url)
    if not save_article(article):
        abort(400)

    return "OK"


@app.route('/favicon.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.png')

