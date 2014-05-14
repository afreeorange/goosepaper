import json
import os

import arrow
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
from goosepaper import app, log, db
from goosepaper.helpers import extract, save_article, mongo_object_to_dict
from goosepaper.models import SavedArticle, DomainStatistics, WordStatistics
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
        return '401', 401
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
        return '401', 401
    id = request.headers['Id'].strip()

    # Set or unset the favorites attribute depending on request method
    action = {'PUT': True, 'DELETE': False}
    SavedArticle.objects.get_or_404(id__exact=id).update(set__favorite=action[request.method])
    log.info('%s %s in favorites' % (id, request.method))
    return '200', 200


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
            return '500', 500
        else:
            log.info('%s deleted' % id)
    return 'Removed'


@app.route('/search/<string:term>/page/<int:number>')
@app.route('/search/<string:term>')
def search(term, number=1):
    term = term.strip()

    if len(term) < 3:
        return jsonify({'error': 'Search term must be longer than 2 characters'})

    paginator = Pagination(SavedArticle.objects(Q(title__icontains=term)  | 
                                                Q(domain__icontains=term) | 
                                                Q(body__icontains=term)).exclude('body').order_by('-sent'), 
                                                number, 
                                                app.config['ARTICLES_PER_PAGE'])
    return render_template('list.html', paginator=paginator, term=term)


@app.route('/export')
def export():
    export_list = {
        'unread': SavedArticle.objects(archived=False),
        'archived': SavedArticle.objects(archived=True),
        'favorited': SavedArticle.objects(favorite=True)
    }
    return render_template('export.html', list=export_list)


@app.route('/api/statistics/words')
def api_stats_words():
    map_f = """
        function() { 
            var words = this.body_plain.match(/[a-zA-Z]{3,}/g);
            if (words === null) {
                return;
            };
            for (var i = words.length - 1; i >= 0; i--) {
                emit(words[i], 1);
            };
        }
    """

    reduce_f = """
        function(key, values) {
            return Array.sum(values);
        }
    """

    stats = {}
    # results = list(SavedArticle.objects.map_reduce(map_f, reduce_f, {'merge': 'stats_words'}))
    
    for article in WordStatistics.objects().order_by('-word').limit(250):
        print mongo_object_to_dict(article)

    return jsonify(stats)


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
        return render_template('list.html', paginator=paginator)

    # Only other method allowed at this point is POST. 
    # Check for 'Article' header and get the URL.
    if 'Article' not in request.headers:
        return '401', 401
    url = request.headers['Article'].strip()

    # Attempt to extract and save article
    article = extract(url)
    saved_article = save_article(article)
    if not saved_article:
        return '400', 400

    return '201', 201


@app.route('/favicon.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.png')
