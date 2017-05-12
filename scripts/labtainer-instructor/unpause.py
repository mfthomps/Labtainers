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

# Filename: unpause.py
# Description:
# This is the script to be run by the instructor to unpause container(s).
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#

import glob
import json
import md5
import os
import re
import subprocess
import sys
import time
import zipfile
from netaddr import *

instructor_cwd = os.getcwd()
student_cwd = instructor_cwd.replace('labtainer-instructor', 'labtainer-student')
# Append Student CWD to sys.path
sys.path.append(student_cwd)

import ParseStartConfig
import logging
import LabtainerLogging

LABS_ROOT = os.path.abspath("../../labs/")

# Error code returned by docker inspect
SUCCESS=0
FAILURE=1

def DoUnpause(start_config, mycwd, labname):
    host_home_xfer = start_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed
    labutils.logger.DEBUG("DoUnpause Multiple Containers and/or multi-home networking")

    # Reach here - Everything is OK - spawn terminal for each container based on num_terminal
    for name, container in start_config.containers.items():
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        container_user         = container.user

        command = "docker unpause %s" % mycontainer_name
        labutils.logger.DEBUG("command is (%s)" % command)
        os.system(command)

    return 0


# Usage: unpause.py <labname>
# Arguments:
#    <labname> - the lab to start
def main():
    num_args = len(sys.argv)
    if num_args < 2:
        sys.stderr.write("Usage: unpause.py <labname>\n")
        sys.exit(1)

    labname = sys.argv[1]
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname)
    labutils.logger.INFO("Begin logging unpause.py for %s lab" % labname)
    labutils.logger.DEBUG("Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd))
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    labutils.logger.DEBUG("current working directory for %s" % mycwd)
    labutils.logger.DEBUG("current user's home directory for %s" % myhomedir)
    labutils.logger.DEBUG("ParseStartConfig for %s" % labname)
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config")
    start_config_path = os.path.join(config_path,"start.config")

    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, "instructor", labutils.logger)

    DoUnpause(start_config, mycwd, labname)

    return 0

if __name__ == '__main__':
    sys.exit(main())

