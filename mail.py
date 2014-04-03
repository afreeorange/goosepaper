# This doesn't work...

import re
import fileinput
import subprocess
import shlex
import sys

project_root = '/path/to/project'
sys.path.append(project_root)

# Get STDIN, get first match
gruber_url_pattern = re.compile(ur'Subject: ((?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019])))')
lines = fileinput.input()
matches = gruber_url_pattern.findall(lines[0])
url = matches[0][0]

# Save it!
command = shlex.split('source %s/bin/activate && %s/save.py --url=%s' % (project_root, project_root, url))
proc = subprocess.Popen(command, stdout = subprocess.PIPE)
proc.communicate()
