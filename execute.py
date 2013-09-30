#!/usr/bin/python

import pexpect
import sys

if (len(sys.argv) < 5):
    print("Not enough args supplied!")
    sys.exit(1)

script    = sys.argv[1]
argstring = sys.argv[2]
log       = file(sys.argv[3],"a")
password  = sys.argv[4]
cmd='./'+ script + ' ' + argstring

#print(script)
#print(argstring)
#print(password)
#print(cmd)

child = pexpect.spawn(cmd)
child.expect('Password: ')
child.sendline(password)
child.logfile = sys.stdout

child.wait()
child.close()

sys.exit(child.exitstatus)


