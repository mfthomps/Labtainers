#!/usr/bin/env python
'''
A simple bot fetch web pages
just keep logging in, listing a directory and logging out.
'''
import sys
import time
import logging
import subprocess
'''

'''
LOGFILE = "/tmp/webbot.log"
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)
logging.debug("sleeping")
time.sleep(10)
logging.debug("hi")

while True:
    cmd='wget http://172.25.0.2/index.html -O index.html'
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_string = child.stderr.read().strip()
    output = child.stdout.read().strip()
    logging.debug(error_string)
    logging.debug(output)
    time.sleep(1)

    cmd='wget http://172.25.0.2/link1.html'
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_string = child.stderr.read().strip()
    output = child.stdout.read().strip()
    logging.debug(error_string)
    logging.debug(output)
    time.sleep(1)

