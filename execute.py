#!/usr/bin/python

import pexpect
import sys

print(len(sys.argv))

if (len(sys.argv) < 4):
    print("Not enough args supplied!")
	sys.exit(1)

script    = sys.argv[1]
argstring = sys.argv[2]
password  = sys.argv[3]

print(script)
print(argstring)
print(password)

# child = pexpect.spawn('./'+ script + ' ' + argstring)
# child.expect('Password:')
# child.sendline(password)