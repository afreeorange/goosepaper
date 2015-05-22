# coding: utf-8

from datetime import datetime
from goosepaper import db


class SavedArticle(db.Document):
    """ A single saved article. Field definitions are done using
        Flask-MongoEngine (see db in __init__.py)
    """
    title = db.StringField(required=True, max_length=255)
    sent = db.DateTimeField(required=True, default=datetime.now())
    url = db.URLField(required=True)
    domain = db.StringField(required=True, max_length=255)
    body = db.StringField(required=True)
    body_plain = db.StringField(required=False)
    authors = db.ListField(required=False)
    summary = db.StringField(required=False)
    favorite = db.BooleanField(required=False, default=False)
    archived = db.BooleanField(required=False, default=False)
    meta = {
        'indexes': ['title', 'domain', 'summary', 'authors']
    }


class DomainStatistics(db.Document):
    # http://docs.mongoengine.org/guide/document-instances.html#document-ids
    # http://docs.mongoengine.org/en/latest/guide/defining-documents.html#working-with-existing-data
    url = db.StringField(primary_key=True)
    value = db.IntField()
    meta = {
        'collection': 'stats_domain'
    }


class WordStatistics(db.Document):
    word = db.StringField(primary_key=True)
    value = db.IntField()
    meta = {
        'collection': 'stats_words'
    }
