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
# Filename: moreterm.py
# Description:
# This is the script to be run by the student to spawn more terminals.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#
# It will perform the following tasks:
# a. If the lab has only one container, only one terminal for that
#    container will be spawned
# b. If the lab has multiple containers, the number of terminals
#    specified in the start.config will be used, unless
#    the user passed the optional argument specifying the number of
#    terminal

import glob
import json
import md5
import os
import re
import subprocess
import sys
import time
import zipfile
import ParseStartConfig
import labutils
import logging
import LabtainerLogging

LABS_ROOT = os.path.abspath("../../labs/")

def DoMoreterm(start_config, mycwd, labname, container, num_terminal):
    mycontainer_name = '%s.%s.student' % (labname, container)
    if not labutils.IsContainerCreated(mycontainer_name):
        labutils.logger.ERROR('container %s not found' % mycontainer_name)
        exit(1)
    for x in range(num_terminal):
        spawn_command = "gnome-terminal -x docker exec -it %s bash -l &" % mycontainer_name
        labutils.logger.ERROR("spawn_command is (%s)" % spawn_command)
        os.system(spawn_command)

    return 0

def usage():
    sys.stderr.write("moreterm.py <labname> [<container>] [<requested_term>]\n")
    exit(1)

# Usage: (see usage)
def main():
    num_args = len(sys.argv)
    container = None
    requested_term = 1
    if num_args < 2:
        usage()
    elif num_args == 2:
        requested_term = 0
        container = sys.argv[1]
    elif num_args == 3:
        if type(sys.argv[2]) is int:
            requested_term = int(sys.argv[2])
            container = sys.argv[1]
        else:
            container = sys.argv[2]
    elif num_args == 4:
        requested_term = int(sys.argv[3])
        container = sys.argv[2]
    else:
        usage()

    labname = sys.argv[1]
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname)
    labutils.logger.INFO("Begin logging moreterm.py for %s lab" % labname)
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    labutils.logger.DEBUG("current working directory for %s" % mycwd)
    labutils.logger.DEBUG("current user's home directory for %s" % myhomedir)
    labutils.logger.DEBUG("ParseStartConfig for %s" % labname)
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config")
    start_config_path = os.path.join(config_path,"start.config")

    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, "student")

    DoMoreterm(start_config, mycwd, labname, container, requested_term)

    return 0

if __name__ == '__main__':
    sys.exit(main())

