#!/usr/bin/env python

# Filename: stop.py
# Description:
# This is the stop script to be run by the instructor.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#

import getpass
import os
import re
import subprocess
import sys
import zipfile

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

# CopyChownGradesFile
def CopyChownGradesFile(mycwd, start_config, container_name, container_image, container_user):
    host_home_xfer = start_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed

    username = getpass.getuser()
    grade_filename = '/home/%s/grades.txt' % container_user
    command = "docker cp %s:%s /home/%s/%s" % (container_name, grade_filename, username, host_home_xfer)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CopyChownGradesFile: Result of subprocess.Popen exec cp grades.txt file is %s" % result
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CopyChownGradesFile Container %s fail on executing cp grades.txt file!\n" % container_name)
        sys.exit(1)

    # Change ownership to defined user $USER
    command = "sudo chown %s:%s /home/%s/%s/grades.txt" % (username, username, username, host_home_xfer)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CopyChownGradesFile: Result of subprocess.Popen exec chown grades.txt file is %s" % result
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CopyChownGradesFile Container %s fail on executing chown grades.txt file!\n" % container_name)
        sys.exit(1)


# Stop my_container_name container
def StopMyContainer(mycwd, start_config, container_name):
    command = "docker stop %s 2> /dev/null" % container_name
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call StopMyContainer stop is %s" % result
    return result

# Check to see if my_container_name container has been created or not
def IsContainerCreated(mycontainer_name):
    command = "docker inspect -f {{.Created}} %s 2> /dev/null" % mycontainer_name
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call IsContainerCreated is %s" % result
    return result

def DoStop(start_config, mycwd, labname):
    host_home_xfer = start_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed
    #print "Do: STOP Multiple Containers and/or multi-home networking"

    for name, container in start_config.containers.items():
        mycontainer_name  = container.full_name
        container_user    = container.user
        mycontainer_image = container.image_name
        haveContainer     = IsContainerCreated(mycontainer_name)
        #print "IsContainerCreated result (%s)" % haveContainer

        # IsContainerCreated returned FAILURE if container does not exists
        # error: can't stop non-existent container
        if haveContainer == FAILURE:
            sys.stderr.write("ERROR: DoStop Container %s does not exist!\n" % mycontainer_name)
        else:
            # The grades.txt can be found in container named start_config.grade_container
            # The 'Instructor.py' should have been run inside that container already
            # and that will create grades.txt file of the result
            if mycontainer_name == start_config.grade_container:
                CopyChownGradesFile(mycwd, start_config, mycontainer_name, mycontainer_image, container_user)
            # Stop the container
            StopMyContainer(mycwd, start_config, mycontainer_name)

    return 0

# Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
def CreateHostHomeXfer(host_xfer_dir):
    # remove trailing '/'
    host_xfer_dir = host_xfer_dir.rstrip('/')
    #print "host_home_xfer directory (%s)" % host_xfer_dir
    if os.path.exists(host_xfer_dir):
        # exists but is not a directory
        if not os.path.isdir(host_xfer_dir):
            # remove file then create directory
            os.remove(host_xfer_dir)
            os.makedirs(host_xfer_dir)
        #else:
        #    print "host_home_xfer directory (%s) exists" % host_xfer_dir
    else:
        # does not exists, create directory
        os.makedirs(host_xfer_dir)

def StopLab(labname):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config")
    start_config_path = os.path.join(config_path,"start.config")

    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, "instructor")

    # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
    host_xfer_dir = '%s/%s' % (myhomedir, start_config.host_home_xfer)
    CreateHostHomeXfer(host_xfer_dir)

    DoStop(start_config, mycwd, labname)

    # Inform user where results are stored
    print "Results (grades.txt) stored in directory: %s" % host_xfer_dir

# Usage: stop.py <labname>
# Arguments:
#    <labname> - the lab to stop
def main():
    #print "stop.py -- main"
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: stop.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    StopLab(labname)

    return 0

if __name__ == '__main__':
    sys.exit(main())

