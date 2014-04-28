from datetime import datetime
import json
import os

from flask import (
    abort, 
    Flask, 
    jsonify, 
    render_template, 
    request, 
    Response,
    send_from_directory
)
from flask.ext.mongoengine import MongoEngine, Pagination
from goosepaper import app, log
from goosepaper.helpers import extract, save_article, mongo_object_to_dict
from goosepaper.models import SavedArticle
from mongoengine import Q


@app.route('/archive/page/<int:number>')
@app.route('/archive/page')
@app.route('/archive', methods=['PUT', 'DELETE', 'GET'])
def archive(number=1):
    """ Manage archive """
    if request.method == 'GET':
        paginator = Pagination(SavedArticle.objects(archived=True).order_by('-sent'), 
                               number, 
                               app.config['ARTICLES_PER_PAGE'])
        return render_template('list.html', paginator=paginator)

    # Get the ID. Abort if not supplied in headers.
    if 'Id' not in request.headers:
        log.error('article ID not provided for archive')
        abort(401)
    id = request.headers['Id'].strip()

    # Set or unset the archive attribute depending on request method
    action = {'PUT': True, 'DELETE': False}
    SavedArticle.objects.get_or_404(id__exact=id).update(set__archived=action[request.method])
    log.info('%s %s in archive' % (id, request.method))
    return '200', 200


@app.route('/favorites/page/<int:number>')
@app.route('/favorites/page')
@app.route('/favorites', methods=['PUT', 'DELETE', 'GET'])
def favorites(number=1):
    """ Manage favorites """
    if request.method == 'GET':
        paginator = Pagination(SavedArticle.objects(favorite=True).order_by('-sent'), 
                               number, 
                               app.config['ARTICLES_PER_PAGE'])
        return render_template('list.html', paginator=paginator)

    # Get the ID. Abort if not supplied in headers.
    if 'Id' not in request.headers:
        log.error('article ID not provided for favorites')
        abort(401)
    id = request.headers['Id'].strip()

    # Set or unset the favorites attribute depending on request method
    action = {'PUT': True, 'DELETE': False}
    SavedArticle.objects.get_or_404(id__exact=id).update(set__favorite=action[request.method])
    log.info('%s %s in favorites' % (id, request.method))
    return "200", 200


@app.route('/articles/<id>', methods=['GET', 'DELETE'])
def article(id=None):
    """ Display or remove a single saved article """
    article = SavedArticle.objects.get_or_404(id__exact=id)

    # Display or delete the article depending on request method
    if request.method == 'GET':
        return render_template('article.html', article=article)
    elif request.method == 'DELETE':
        try:
            article.delete()
        except Exception, e:
            return '400', abort(500)
        else:
            log.info('%s deleted' % id)
    return "Removed"


@app.route('/search/<string:term>/page/<int:number>')
@app.route('/search/<string:term>')
def search(term, number=1):
    term = term.strip()

    if len(term) < 4:
        return jsonify({'error': 'Search term must be longer than 3 characters'})

    paginator = Pagination(SavedArticle.objects(Q(title__icontains=term)  | 
                                                Q(domain__icontains=term) | 
                                                Q(body__icontains=term)).exclude('body').order_by('-sent'), 
                                                number, 
                                                app.config['ARTICLES_PER_PAGE'])
    return render_template("list.html", paginator=paginator, term=term)

    # results = []
    # for article in articles:
    #     results.append(mongo_object_to_dict(article))

    # http://flask.pocoo.org/docs/security/#json-security
    # return Response(json.dumps(results), mimetype='application/json')


@app.route('/page/<int:number>')
@app.route('/articles')
@app.route('/index')
@app.route('/', methods=['POST', 'GET'])
def index(number=1):
    """ Save a URI or show some information on how to do so """
    # Display articles if GET-ting a page
    if request.method == 'GET':
        paginator = Pagination(SavedArticle.objects(archived=False).order_by('-sent'), 
                               number, 
                               app.config['ARTICLES_PER_PAGE'])
        return render_template("list.html", paginator=paginator)

    # Only other method allowed at this point is POST. 
    # Check for 'Article' header and get the URL.
    if 'Article' not in request.headers:
        abort(401)
    url = request.headers['Article'].strip()

    # Attempt to extract and save article
    article = extract(url)
    saved_article = save_article(article)
    if not saved_article:
        return '400', 400

    return jsonify(saved_article), 201


@app.route('/favicon.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.png')
