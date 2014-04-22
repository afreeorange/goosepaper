from datetime import datetime
from sys import exit

from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask.ext.mongoengine import MongoEngine
from logbook import FileHandler, Logger


app = Flask(__name__)
app.config.from_object('settings')

# Set up routing appropriately
if app.config['APPLICATION_ROOT']:
	from werkzeug.wsgi import DispatcherMiddleware
	routed_app = DispatcherMiddleware(app, {app.config['APPLICATION_ROOT']: app})
else:
	routed_app = app

# Set up compressed CSS and JS
assets = Environment(app)
assets.register('scripts', Bundle('js/goosepaper.js',
                                  filters='jsmin', output='js/packed.js'))
assets.register('stylesheets', Bundle('css/goosepaper.css', 
                                  filters='cssmin', output='css/packed.css'))

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
    print "If on another server or port, look at settings.py."
    exit(1)

from goosepaper import views, models, filters
if __name__ == '__main__':
    app.run()
