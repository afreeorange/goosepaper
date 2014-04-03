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
    summary = db.StringField(required=False)
