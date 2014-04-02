from datetime import datetime
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.script import Manager
from jinja2 import Environment

app = Flask(__name__)
app.config.from_object('settings')

from things_i_read import views, models

# Set up routing appropriately
if app.config['APPLICATION_ROOT']:
	from werkzeug.wsgi import DispatcherMiddleware
	routed_app = DispatcherMiddleware(app, {app.config['APPLICATION_ROOT']: app})
else:
	routed_app = app

# Set up database connection
try:
    db = MongoEngine(app)
except ConnectionError, e:
    print str(e)
    print "----"
    print "Are you sure your MongoDB instance is running?"
    print "If on another server or port, look at settings.py."
    exit(1)

manager = Manager(app)
