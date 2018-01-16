#!/usr/bin/env python
'''
A simple bot to login to a telnet server, change a password, and then
just keep logging in, listing a directory and logging out.
'''
import sys
from subprocess import PIPE, Popen
import logging

ON_POSIX = 'posix' in sys.builtin_module_names

def doLogin(uid, passwd):
    retval = True
    logging.debug("in doLogin for %s %s" % (uid, passwd))
    command = 'sshpass -p"%s" ssh -tt %s@172.20.0.3 exit' % (passwd, uid)
    #print "command is (%s)" % command
    p = Popen(command, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE, bufsize=1, close_fds=ON_POSIX)

    logging.debug("after cmd: %s" % command)
    output = p.communicate()
    got = output[1]
    #got = p.stderr.read()
    #print "Got is (%s)" % got
    logging.debug('stderr read, %s' % got)
    if 'Permission denied' in got:
        #print('login incorrect')
        retval = False
    elif 'Connection closed' in got or 'Connection reset by peer' in got:
        #print('Connection closed triggered')
        retval = True
    else:
        print('Sucess!')
    return retval, p


'''
First loging and chnage the password.  NEWPWD should be replaced by
a student-specific value.
'''
if len(sys.argv) != 2:
    print('./bot.py <User ID>')
LOGFILE = "/tmp/bot.log"
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)
uid = sys.argv[1]
count = 1
while True:
    testpwd = '%s%s' % (uid, count)
    result, p = doLogin(uid, testpwd)
    if result:
        print "Got Connection closed"
        break
    else:
        print("try user: %s passwd: %s -- permission denied, count=%s" % (uid, testpwd, count))
    p.wait()
    count = count + 1

