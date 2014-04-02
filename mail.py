#!bin/python
"""
Will attempt to pick up URL from STDIN
"""
from sys import exit
from things_i_read import views
import fileinput

f = open('/tmp/test.txt', 'w')
f.write('HHIHIHIHIHIHIHI\n')

for line in fileinput.input():
    f.write(line)
