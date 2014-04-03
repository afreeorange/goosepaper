""" Goosepaper Saver!
Usage:
  save.py (--url=<url>)

Options:
  --url=<url>  The URL you'd like to save.

"""
from docopt import docopt
from sys import exit
from goosepaper.helpers import cli_save

# Get the URL to save
arguments = docopt(__doc__)
url = arguments['--url']

# And, you know, save it
cli_save(url)
