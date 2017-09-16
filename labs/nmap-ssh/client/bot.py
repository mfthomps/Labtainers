#!/usr/bin/env python
'''
A simple bot to login to a telnet server, change a password, and then
just keep logging in, listing a directory and logging out.
'''
import sys
from subprocess import PIPE, Popen
from threading  import Thread
import time
import logging
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names
def enqueue_output(out, queue):
    logging.debug("enqueue_output")
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def readUntil(val_list, q, stderr_q=None):
    retval = None
    # read line without blocking
    logging.debug("readUntil")
    line = ''
    done = False
    while not done:
        if stderr_q is not None:
            try:
                line = stderr_q.get_nowait()
                if line is not None and len(line) > 0:
                    logging.debug('stderr: '+line)
            except Empty:
                pass

        try:  
            line = q.get_nowait() # or q.get(timeout=.1)
            for val in val_list:
                if val in line:
                    done = True
                    retval = val
                    print('got readuntil for %s' % val)
                    break
        except Empty:
            #print('no output yet')
            time.sleep(1)
        else: # got line
            logging.debug(line)
            #print line
    return retval

def doLogin(passwd):
    retval = True
    logging.debug("in doLogin")
    p = Popen(['telnet', '172.25.0.1'], stdout=PIPE, stdin=PIPE, stderr=PIPE, bufsize=1, close_fds=ON_POSIX)
    q = Queue()
    stderr_q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    stderr_t = Thread(target=enqueue_output, args=(p.stderr, stderr_q))
    t.daemon = True # thread dies with the program
    t.start()

    logging.debug("after start")
    readUntil(['Ubuntu'], q, stderr_q)
    p.stdin.write('ubuntu\n')
    readUntil(['server login'] , q)
    p.stdin.write('%s\n' % passwd)
    got = readUntil(['* Support:', 'Login incorrect'], q)
    if got == 'Login incorrect':
        print('found login incorrect')
        retval = False
    return retval, p,q


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
result, p, q = doLogin('ubuntu')
if result:
    cmd = "echo 'ubuntu:%s' | sudo chpasswd\n" % newpwd
    logging.debug('cmd is '+cmd)
    p.stdin.write(cmd)
    time.sleep(1)
    logging.debug('changed pwd??')
    p.stdin.write('ls\n')
    readUntil(['filetoview.txt'], q)
    p.stdin.write('exit\n')
    time.sleep(1)
    p.wait()
else:
    print('failed login, try new password')
    p.stdin.write('ubuntu\n')
    readUntil(['server login'] , q)
    p.stdin.write('%s\n' % newpwd)

while True:
    result, p, q = doLogin(newpwd)
    p.stdin.write('ls\n')
    readUntil(['filetoview.txt'], q)
    p.stdin.write('exit\n')
    p.wait()
    time.sleep(5)


