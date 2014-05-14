from datetime import datetime
from sys import exit
import locale
import os

import arrow
from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask.ext.mongoengine import MongoEngine
from mongoengine import ConnectionError
from logbook import FileHandler, Logger


app = Flask(__name__)
app.config.from_object('settings')


# Set locale
locale.setlocale(locale.LC_ALL, app.config['LOCALE'])


# Set up routing appropriately
if app.config['APPLICATION_ROOT']:
	from werkzeug.wsgi import DispatcherMiddleware
	routed_app = DispatcherMiddleware(app, {app.config['APPLICATION_ROOT']: app})
else:
	routed_app = app


# Some Jinja2 helper functions 
app.jinja_env.globals.update(export_datestamp=lambda: arrow.now().format('dddd, D MMMM YYYY, h:m a'))
app.jinja_env.globals.update(iso_timestamp=lambda: arrow.now())


# Set up logging
log_handler = FileHandler('logs/goosepaper.log')
log_handler.push_application()
log = Logger('goosepaper')


# Set up database connection
try:
    db = MongoEngine(app)
except ConnectionError, e:
    print str(e)
    print "----"
    print "Are you sure your MongoDB instance is running?"
    print "If it's on another server or port, modify settings.py."
    exit(1)


from goosepaper import views, models, filters
if __name__ == '__main__':
    app.run()
