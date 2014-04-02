HOST="127.0.0.1"
PORT=5000
DEBUG = True
MONGODB_SETTINGS = {'DB': "things_i_read", 'PORT': 27017}

# Use if you want to host at localhost:5000/things_i_read
# If you're on a dedicated subdomain, comment this out entirely.
APPLICATION_ROOT = "/things_i_read"

from datetime import datetime
CURRENT_YEAR = datetime.now().strftime("%Y")
COPYRIGHT_MESSAGE = '&copy;', CURRENT_YEAR

CSRF_ENABLED = True
SECRET_KEY = "r/hV9t14EwGfUyTmSGy1jYFfQx526ToQ"

