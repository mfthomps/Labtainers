#!/usr/bin/env python
import os
import time
import subprocess
import logging
LOGFILE = "./historian.log"
print("logging to %s" % LOGFILE)
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, 
                         format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%y-%m-%d %H:%M:%S')
logging.debug("Starting historian")

cmd = 'manage_plc status'
while True:
    time.sleep(20)
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].strip()) > 0:
         logging.debug('%s' % output[0].strip()) 
    
