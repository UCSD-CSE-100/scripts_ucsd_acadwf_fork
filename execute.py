#!/usr/bin/python

import pexpect
import sys

if (len(sys.argv) < 4):
    print("Not enough args supplied!")
    sys.exit(1)

script    = sys.argv[1]
argstring = sys.argv[2]
password  = sys.argv[4]
cmd='./'+ script + ' ' + argstring

#print(script)
#print(argstring)
#print(password)
#print(cmd)

with open(sys.argv[3], 'a') as log:
    child = pexpect.spawn(cmd)
    child.expect('Password: ')
    child.sendline(password)
    child.expect(pexpect.EOF,10800)
    log.write(child.before)
    
child.close()    
sys.exit(child.exitstatus)


