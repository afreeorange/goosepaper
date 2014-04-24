HOST="0.0.0.0"
PORT=5000
DEBUG = True
MONGODB_SETTINGS = {'DB': "goosepaper", 'PORT': 27017}
NUMBER_OF_WORKERS = 10

# Use if you want to host at localhost:5000/things_i_read
# If you're on a dedicated subdomain, comment this out entirely.
APPLICATION_ROOT = "/goosepaper"

from datetime import datetime
CURRENT_YEAR = datetime.now().strftime("%Y")
COPYRIGHT_MESSAGE = '&copy;', CURRENT_YEAR

CSRF_ENABLED = True
SECRET_KEY = "r/hV9t14EwGfUyTmSGy1jYFfQx526ToQ"

SUMMARY_LENGTH = 250
ARTICLES_PER_PAGE = 50

