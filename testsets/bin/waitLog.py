#!/usr/bin/env python3
#
# Wait until the given log file reports success or failure
#
import os
import sys
import time
logfile = sys.argv[1]
if not os.path.isfile(logfile):
    print('No log file found at %s' % logfile)
    exit(1)
result = None
count = 0
while result is None:
   time.sleep(5)
   with open(logfile) as fh:
       lines = fh.readlines()
       last = lines[-1]
       if 'Success' in last:
           result = True
       elif 'test failed' in last:
           result = False
   count += 1
   if count > 2000:
       print('waitLog timed out on %s' % logfile)
       exit(1)
if not result:
    print('Failure found in %s' % logfile)
    exit(1)
print('Done')
exit(0)
