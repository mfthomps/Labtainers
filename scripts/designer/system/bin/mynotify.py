#!/usr/bin/env python
import os
import time
import logging
from inotify_simple import INotify, flags
logger = logging.getLogger('mynotify')
hdlr = logging.FileHandler('/tmp/mynotify.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)


class WatchType():
    def __init__(self, path, flag):
        self.path = path
        self.flag = flag

def showMask(mask):
    if mask & flags.CREATE:
        print('CREATE')
    if mask & flags.ACCESS:
        print('ACCESS')


def get_flag(flag):
    if flag == 'CREATE':
        return flags.CREATE
    elif flag == 'ACCESS':
        return flags.ACCESS
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
            watch = WatchType(parts[0], parts[1])
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
        checklocalinfile = os.path.join(results, 'checklocal.stdin.%s' % ts)
        if not os.path.isfile(checklocaloutfile):
            ''' no file, if from previous second, use that as hack to merge with output from command '''
            now = now -1
            ts = time.strftime('%Y%m%d%H%M%S', time.localtime(now))
            tmpfile = os.path.join(results, 'checklocal.stdout.%s' % ts )
            if os.path.isfile(tmpfile):
                checklocaloutfile = os.path.join(results, 'checklocal.stdout.%s' % ts )
                checklocalinfile = os.path.join(results, 'checklocal.stdin.%s' % ts)
            
        cmd = '%s %s %s >> %s 2>/dev/null' % (checklocal, watch.path, watch.flag, checklocaloutfile)
        logger.debug('cmd is %s' % cmd)
        os.system(cmd)
                         
