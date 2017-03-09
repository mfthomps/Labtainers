#!/usr/bin/env python

# Filename: moreterm.py
# Description:
# This is the script to be run by the instructor to spawn more terminals.
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
from netaddr import *

instructor_cwd = os.getcwd()
student_cwd = instructor_cwd.replace('MyInstructorDocker', 'MyStudentDocker')
print "Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd)
# Append Student CWD to sys.path
sys.path.append(student_cwd)

import ParseStartConfig

LABS_ROOT = os.path.abspath("../../labs/")

# Error code returned by docker inspect
SUCCESS=0
FAILURE=1

def isalphadashscore(name):
    # check name - alphanumeric,dash,underscore
    return re.match(r'^[a-zA-Z0-9_-]*$', name):

# Check to see if my_container_name container has been created or not
def IsContainerCreated(mycontainer_name):
    command = "docker inspect -f {{.Created}} %s 2> /dev/null" % mycontainer_name
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call IsContainerCreated is %s" % result
    return result

def DoMoreterm(start_config, mycwd, labname, requested_term):
    host_home_xfer = start_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed
    #print "Do: Moreterm Multiple Containers and/or multi-home networking"

    # Reach here - Everything is OK - spawn terminal for each container based on num_terminal
    for name, container in start_config.containers.items():
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        container_user         = container.user

        # if requested_term != 0 then use it
        if requested_term != 0:
            num_terminal = requested_term
        else:
            num_terminal = container.terminals

        #print "Number of terminal is %d" % num_terminal
        # If the number of terminal is zero -- do not spawn
        if num_terminal != 0:
            for x in range(num_terminal):
                spawn_command = "gnome-terminal -x docker exec -it %s bash -l &" % mycontainer_name
                #print "spawn_command is (%s)" % spawn_command
                os.system(spawn_command)

    return 0


# Usage: moreterm.py <labname> [<requested_term>]
# Arguments:
#    <labname> - the lab to start
#    [<requested_term>] - optional argument to specify the number of terminal to spawn
def main():
    #print "moreterm.py -- main"
    num_args = len(sys.argv)
    if num_args < 2:
        sys.stderr.write("Usage: moreterm.py <labname> [<requested_term>]\n")
        sys.exit(1)
    elif num_args == 2:
        requested_term = 0
    elif num_args == 3:
        requested_term = int(sys.argv[2])
    else:
        sys.stderr.write("Usage: moreterm.py <labname> [<requested_term>]\n")
        sys.exit(1)

    labname = sys.argv[1]
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config")
    start_config_path = os.path.join(config_path,"start.config")

    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, "instructor")

    DoMoreterm(start_config, mycwd, labname, requested_term)

    return 0

if __name__ == '__main__':
    sys.exit(main())

