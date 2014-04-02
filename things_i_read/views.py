from flask import Flask, render_template, request, abort, jsonify
from goose import Goose
from datetime import datetime
from mongoengine import Document, StringField, DateTimeField
from re import split
from things_i_read import app


@app.template_filter('paragraphs')
def paragraphs(body=None):
    paragraphs = split(r'[\n\n]+', body)
    html = '\n'.join([u'<p>%s</p>' % paragraph for paragraph in paragraphs])
    return html


@app.template_filter('relative_date')
def relative_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"


class Article(Document):
    """ A single saved article """
    title = StringField(required=True, max_length=255)
    sent = DateTimeField(required=True, default=datetime.now())
    url = StringField(required=True, max_length=255)
    domain = StringField(required=True, max_length=255)
    body = StringField(required=True)


def extract(url=None):
    """ Attempts to extract article from URL """
    g = Goose()
    try:
        article = g.extract(url=url)
    except Exception, e:
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
                 domain=article.domain ).save()


@app.route('/send', methods=['GET', 'POST'])
def send():
    if 'Article' not in request.headers:
        abort(401)

    url = request.headers['Article'].strip()

    # Check if document exists
    if Article.objects(url__exact=url):
        return "Exists"

    article = extract(url)
    save_article(article)
    return "OK"


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", 
                           articles=Article.objects().order_by('-sent'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

