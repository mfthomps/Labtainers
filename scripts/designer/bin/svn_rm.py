#!/usr/bin/env python
'''
Use svn to remove a file, and then modify the parent directory
(using a dummy property), so that affected containers get rebuilt.
'''
import os
import sys
import time
if len(sys.argv) != 2:
    print('svn_rm.py path')
path = sys.argv[1]
cmd = 'svn rm %s' % path
print cmd
os.system(cmd)
if '/' in path:
    parent = os.path.dirname(path)
else:
    parent = '../'

print('parent is %s' % parent)
cmd = "svn propset file_rm_date '%s' %s" % (time.time(), parent)
print cmd
os.system(cmd)
