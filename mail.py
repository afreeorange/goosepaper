import fileinput
import re
import urllib
import httplib

host = 'localhost'
port = 5000
endpoint = '/'

# Get STDIN, get first match
url_pattern = re.compile(ur'Subject: ((?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019])))')
lines = fileinput.input()
matches = url_pattern.findall(lines[0])
url = matches[0][0]

# Could use requests module, but cannot assume system-wide install
params = ''
headers = {'article': url}
conn = httplib.HTTPConnection(host, port)
conn.request("POST", endpoint, params, headers)
response = conn.getresponse()
print response.read()
