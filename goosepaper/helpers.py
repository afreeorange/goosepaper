from datetime import datetime

from goose import Goose
from goosepaper.models import Article


def extract(url=None):
    """ Attempts to extract article from URL """
    g = Goose()
    try:
        article = g.extract(url=url)
    except Exception, e:
        print "Oops! The goose says:", str(e)
        return False

    article.url = url
    return article


def save_article(article):
    """ Save article to MongoDB instance """

    # Check if document exists. If it does, simply update the save date.
    if Article.objects(url__exact=article.url):
        Article.objects.get(url__exact=article.url).update(set__sent=str(datetime.now()))
        return True

    # Else, insert record
    try:
        Article( title=article.title,
                 sent=str(datetime.now()),
                 url=article.url,
                 body=article.cleaned_text,
                 domain=article.domain.replace('www.',''),
                 summary=article.cleaned_text[:255] ).save()
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
