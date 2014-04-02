""" Article Saver
Usage:
  save.py (--url=<url>)

Options:
  --url=<url>  The URL you'd like to save.

"""
from docopt import docopt
from sys import exit
from goosepaper import views

# Get the URL to save
arguments = docopt(__doc__)
url = arguments['--url']

# Check if document exists
if views.Article.objects(url__exact=url):
    print "You've saved this article before."
    exit(0)

# Extract
article = views.extract(url)

# Save!
save_article(article)
