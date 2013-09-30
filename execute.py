#!/usr/bin/python

import pexpect
import sys

if (len(sys.argv) < 4):
    print("Not enough args supplied!")
    sys.exit(1)

script    = sys.argv[1]
argstring = sys.argv[2]
password  = sys.argv[3]
cmd='./'+ script + ' ' + argstring

#print(script)
#print(argstring)
#print(password)
#print(cmd)

child = pexpect.spawn(cmd)
child.expect('Password: ')
child.sendline(password)

import time

while child.isalive():
    time.sleep(1)

