from datetime import datetime
from sys import exit

from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object('settings')

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

from goosepaper import views, models, filters
if __name__ == '__main__':
    app.run()

