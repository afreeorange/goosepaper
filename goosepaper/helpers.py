# coding: utf-8

import arrow
from goosepaper import app, db, log
from goosepaper.models import SavedArticle
from newspaper import Article


def extract(url=None, keep_html=True):
    """ Attempts to extract article from URL """
    a = Article(url, keep_article_html=keep_html)
    try:
        a.download()
    except Exception, e:
        log.error('Error downloading %s: %s' % (url, str(e)))
    else:
        try:
            a.parse()
        except Exception, e:
            log.error('Error parsing %s: %s' % (url, str(e)))
            return False
        else:
            log.info('Extracted %s' % url)
            return a


def save_article(article):
    """ Save article to MongoDB instance """

    # Check if document exists. If it does, simply update the save date.
    if SavedArticle.objects(url__exact=article.url):
        a = SavedArticle.objects.get(url__exact=article.url)
        a.update(set__sent=str(arrow.now()))
        log.info('%s has updated timestamp' % str(a.id))

    # Else, insert record
    else:
        try:
            a = SavedArticle(title=article.title,
                             sent=str(arrow.now()),
                             url=article.url,
                             body=article.article_html,
                             body_plain=article.text,
                             authors=article.authors,
                             domain=article.source_url.replace('https://', '').replace('http://', '').replace('www.', ''),
                             summary=article.text[:app.config['SUMMARY_LENGTH']]).save()
        except Exception, e:
            log.error('Error saving article: %s' % str(e))
            return {}
        else:
            log.info('%s saved from %s' % (str(a.id), article.url))

    # Return a small JSON representation of article
    return {
        'id': str(a.id),
        'title': a.title,
        'summary': a.summary,
        'domain': a.domain
    }


def cli_save(url):
    """ Helper for CLI scripts """

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
    """ Convert a MongoEngine object to a dictionary """
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
            return_data.append((field_name, ','.join([str(i) for i in data])))
        elif isinstance(obj._fields[field_name], db.DateTimeField):
            return_data.append((field_name, str(data.isoformat())))
        elif isinstance(obj._fields[field_name], db.BooleanField):
            return_data.append((field_name, data))
        else:
            pass

    return dict(return_data)
