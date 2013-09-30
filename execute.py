#!/usr/bin/python

import pexpect
import sys

print(len(sys.argv))

script    = sys.argv[1]
argstring = sys.argv[2]
password  = sys.argv[3]


# child = pexpect.spawn('./'+ script + ' ' + argstring)
# child.expect('Password:')
# child.sendline(password)