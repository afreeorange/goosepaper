from datetime import datetime

from goose import Goose
from goosepaper.models import Article


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