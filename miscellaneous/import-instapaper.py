"""
Allows me to import URLs from an HTML file exported from Instapaper
"""

import requests
import sys
from bs4 import BeautifulSoup

API_HOST='http://localhost:5000/'

if len(sys.argv) != 2:
    print "You need to tell me the path to the HTML file"
    sys.exit(1)

soup = BeautifulSoup(open(sys.argv[1]))
for link in soup.select('ol > li > a'):
    print "Trying", link.get('href')[:79], "..."
    
    r = requests.post(API_HOST, headers={'Article': link.get('href')})
    
    if r.status_code != 200:
        print "Error!"
    else:
        print 'OK'
