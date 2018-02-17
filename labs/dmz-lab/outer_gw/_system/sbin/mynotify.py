#!/usr/bin/env python
'''
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
'''
import os
import time
import logging
import subprocess
from inotify_simple import INotify, flags

'''
This runs as a service on the containers. It uses inotify
to catch events defined in the .local/bin/notify file, 
and will invoke checklocal.sh for when those events occur.
We pass the file, the mode the first user in the system to
checklocal.sh   The timestamped output is appended to any
existing checklocal.stdout.... within 1 second of now.
Alternately, the notify file can include an optional output
filename.
 
It dies without a wimper.  Debug by manually running and generating
inotify events.
'''
logger = logging.getLogger('mynotify')
hdlr = logging.FileHandler('/tmp/mynotify.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)


class WatchType():
    def __init__(self, path, flag, outfile=None):
        self.path = path
        self.flag = flag
        self.outfile = outfile

def showMask(mask):
    if mask & flags.CREATE:
        print('CREATE')
    if mask & flags.ACCESS:
        print('ACCESS')
    if mask & flags.OPEN:
        print('OPEN')


def get_flag(flag):
    if flag == 'CREATE':
        return flags.CREATE
    elif flag == 'ACCESS':
        return flags.ACCESS
    elif flag == 'OPEN':
        return flags.OPEN
    else:
        return None

def get_first_user():
    with open('/etc/passwd') as fh:
        for line in fh:
            parts = line.strip().split(':')
            if parts[2] == '1000':
                return parts[0]
    return None

logger.debug('Start mynotify')
watches = {}

inotify = INotify()
first_user = get_first_user()
logger.debug('first user is %s' % first_user)
notify_file = '/home/%s/.local/bin/notify' % first_user
checklocal = '/home/%s/.local/bin/checklocal.sh' % first_user
results = '/home/%s/.local/result' % first_user
if not os.path.isfile(notify_file) or not os.path.isfile(checklocal):
    logger.debug('missing checklocal %s or notify %s' % (checklocal, notify_file))
    exit(0)
with open(notify_file) as fh:
    for line in fh:
        if not line.strip().startswith('#'):
            parts = line.strip().split()
            outfile = None
            if len(parts) > 2:
                outfile = parts[2]
            watch = WatchType(parts[0], parts[1], outfile)
            flag = get_flag(watch.flag)
            try:
                wd = inotify.add_watch(watch.path, flag)
                watches[wd] = watch
            except:
                logger.debug('could not add watch for %s %s' % (watch.path, watch.flag))
while True:
    for event in inotify.read():
        print(event)
        showMask(event.mask)
        watch = watches[event.wd]
        logger.debug('path: %s flag: %s' % (watch.path, watch.flag))
        now = time.time()
        ts = time.strftime('%Y%m%d%H%M%S', time.localtime(now))
        checklocaloutfile = os.path.join(results, 'checklocal.stdout.%s' % ts )
        #checklocalinfile = os.path.join(results, 'checklocal.stdin.%s' % ts)
        is_a_file = False
        if watch.outfile is None:
            if not os.path.isfile(checklocaloutfile):
                ''' no file, if from previous second, use that as hack to merge with output from command '''
                now = now -1
                ts = time.strftime('%Y%m%d%H%M%S', time.localtime(now))
                tmpfile = os.path.join(results, 'checklocal.stdout.%s' % ts )
                if os.path.isfile(tmpfile):
                    checklocaloutfile = os.path.join(results, 'checklocal.stdout.%s' % ts )
                    #checklocalinfile = os.path.join(results, 'checklocal.stdin.%s' % ts)
                    is_a_file = True
            else:
                is_a_file = True
        else:
            ''' use output filename from notify list '''
            checklocaloutfile = os.path.join(results, '%s.stdout.%s' % (watch.outfile, ts))
          
        if is_a_file:    
            ''' existing file, append to it '''
            cmd = '%s %s %s %s >> %s 2>/dev/null' % (checklocal, watch.path, watch.flag, first_user, checklocaloutfile)
            os.system(cmd)
            #logger.debug('cmd is %s' % cmd)
        else:
            ''' only write to file if checklocal generates output '''
            cmd = '%s %s %s %s ' % (checklocal, watch.path, watch.flag, first_user)
            child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = child.communicate()
            if len(output[0]) > 0:
                with open(checklocaloutfile, 'w') as fh:
                    fh.write(output[0])
