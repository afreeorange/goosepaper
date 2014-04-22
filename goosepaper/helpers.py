from datetime import datetime

from goose import Goose
from newspaper import Article
from goosepaper import app, db
from goosepaper.models import SavedArticle


def extract(url=None, keep_html=True):
    """ Attempts to extract article from URL """
    a = Article(url, keep_article_html=keep_html)
    a.download()
    a.parse()
    return a


def save_article(article):
    """ Save article to MongoDB instance """

    # Check if document exists. If it does, simply update the save date.
    if SavedArticle.objects(url__exact=article.url):
        SavedArticle.objects.get(url__exact=article.url).update(set__sent=str(datetime.now()))
        return True

    # Else, insert record
    try:
        SavedArticle(title=article.title,
                     sent=str(datetime.now()),
                     url=article.url,
                     body=article.article_html,
                     authors=article.authors,
                     domain=article.source_url.replace('https://', '').replace('http://', '').replace('www.',''),
                     summary=article.text[:app.config['SUMMARY_LENGTH']]).save()
    except Exception, e:
        print "Oops! The goose says:", str(e)
        return False
    else:
        return True


def cli_save(url):
    """ Helper for CLI scripts """
    # Attempt to extract article
    article = extract(url)
    if not article:
        print "Error extracting URL"
        exit(1)

    if not save_article(article):
        print "Database error"
        exit(1)

    print "Saved"
    exit(0)


def mongo_object_to_dict(obj):
    return_data = []
    for field_name in obj._fields:
        data = obj._data[field_name]

        if data is None:
            continue

        if isinstance(obj._fields[field_name], db.ObjectIdField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], db.StringField):
            return_data.append((field_name, data.encode('utf-8')))
        elif isinstance(obj._fields[field_name], db.FloatField):
            return_data.append((field_name, float(data)))
        elif isinstance(obj._fields[field_name], db.IntField):
            return_data.append((field_name, int(data)))
        elif isinstance(obj._fields[field_name], db.ListField):
            return_data.append((field_name, int(data)))
        elif isinstance(obj._fields[field_name], db.DateTimeField):
            return_data.append((field_name, str(data.isoformat())))
        elif isinstance(obj._fields[field_name], db.BooleanField):
            return_data.append((field_name, data))
        else:
            pass

    return dict(return_data)
