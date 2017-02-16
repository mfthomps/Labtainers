#!/usr/bin/env python

# Filename: unpause.py
# Description:
# This is the script to be run by the instructor to unpause container(s).
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
# 2. If the lab has multiple containers and/or multi-home
#    networking, then <labname>.network file is necessary
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
student_cwd = instructor_cwd.replace('MyInstructorDocker', 'MyStudentDocker')
print "Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd)
# Append Student CWD to sys.path
sys.path.append(student_cwd)

import ParseMulti
import ParseStartConfig

# Error code returned by docker inspect
SUCCESS=0
FAILURE=1

def isalphadashscore(name):
    # check name - alphanumeric,dash,underscore
    if re.match(r'^[a-zA-Z0-9_-]*$', name):
        return True
    else:
        return False

# Check to see if my_container_name container has been created or not
def IsContainerCreated(mycontainer_name):
    command = "docker inspect -f {{.Created}} %s 2> /dev/null" % mycontainer_name
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call IsContainerCreated is %s" % result
    return result

def DoUnpauseSingle(start_config, mycwd, labname):
    #print "Do: Moreterm Single Container with default networking"
    container_name = start_config.container_name
    container_image = start_config.container_image
    container_user = start_config.container_user
    host_home_xfer = start_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed
    haveContainer = IsContainerCreated(container_name)
    #print "IsContainerCreated result (%s)" % haveContainer

    # IsContainerCreated returned FAILURE if container does not exists
    if haveContainer == FAILURE:
        sys.stderr.write("ERROR: DoUnpauseSingle Container %s still not created!\n" % container_name)
        sys.exit(1)

    # Reach here - Everything is OK - spawn one terminals by default
    command = "docker unpause %s" % container_name
    #print "command is (%s)" % command
    os.system(command)

    return 0

def DoUnpauseMultiple(start_config, mycwd, labname):
    container_user = start_config.container_user
    host_home_xfer = start_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed
    #print "Do: Moreterm Multiple Containers and/or multi-home networking"

    networkfilename = '%s/%s.network' % (mycwd, labname)
    multi_config = ParseMulti.ParseMulti(networkfilename)

    # Reach here - Everything is OK - spawn terminal for each container based on num_terminal
    for mycontainer_name in multi_config.containers:
        command = "docker unpause %s" % mycontainer_name
        #print "command is (%s)" % command
        os.system(command)

    return 0


# Usage: unpause.py <labname>
# Arguments:
#    <labname> - the lab to start
def main():
    #print "unpause.py -- main"
    num_args = len(sys.argv)
    if num_args < 2:
        sys.stderr.write("Usage: unpause.py <labname>\n")
        sys.exit(1)

    labname = sys.argv[1]
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    startconfigfilename = '%s/start.config' % mycwd
    start_config = ParseStartConfig.ParseStartConfig(startconfigfilename, labname, "instructor")

    networkfilename = '%s/%s.network' % (mycwd, labname)
    # If <labname>.network exists, do multi-containers/multi-home networking
    # else do single container with default networking
    if not os.path.exists(networkfilename):
        DoUnpauseSingle(start_config, mycwd, labname)
    else:
        DoUnpauseMultiple(start_config, mycwd, labname)

    return 0

if __name__ == '__main__':
    sys.exit(main())

