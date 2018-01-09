#!/usr/bin/env python
'''
A simple bot to login to a telnet server, change a password, and then
just keep logging in, listing a directory and logging out.
'''
import sys
from subprocess import PIPE, Popen
import time
import logging

ON_POSIX = 'posix' in sys.builtin_module_names

def doLogin(passwd):
    retval = True
    logging.debug("in doLogin")
    command = 'sshpass -p"%s" ssh -tt ubuntu@172.20.0.3' % passwd
    #print "command is (%s)" % command
    p = Popen(command, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE, bufsize=1, close_fds=ON_POSIX)

    logging.debug("after start")
    got = p.stderr.read()
    #print "Got is (%s)" % got
    if 'Permission denied' in got:
        #print('login incorrect')
        retval = False
    if 'Connection closed' in got:
        #print('Connection closed triggered')
        retval = True
    return retval, p


'''
First loging and chnage the password.  NEWPWD should be replaced by
a student-specific value.
'''
LOGFILE = "/tmp/bot.log"
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)
logging.debug("sleeping")
time.sleep(10)
logging.debug("hi")
newpwd = 'NEWPWD'
count = 1
while True:
    testpwd = '%s%s' % (newpwd, count)
    #print "testpwd is %s" % testpwd
    result, p = doLogin(testpwd)
    if result:
        print "Got Connection closed"
        break
    else:
        print "Still permission denied, count=%s" % count
    p.wait()
    count = count + 1
    #time.sleep(5)

