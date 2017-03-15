#!/usr/bin/env python

# Filename: stop.py
# Description:
# This is the stop script to be run by the student.
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
import ParseStartConfig

LABS_ROOT = os.path.abspath("../../labs/")

# Error code returned by docker inspect
SUCCESS=0
FAILURE=1

# CreateCopyChownZip
def CreateCopyChownZip(mycwd, start_config, container_name, container_image, container_user):
    #TODO: FIX
    host_home_xfer  = start_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed

    # Run 'Student.py' - This will create zip file of the result
#   print "About to call Student.py"
    bash_command = "'cd ; . .profile ; Student.py'"
#   bash_command = "'cd ; . .bash_profile ; Student.py'"
    command = 'docker exec -it %s script -q -c "/bin/bash -c %s" /dev/null' % (container_name, bash_command)
#   print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
#   print "CreateCopyChownZip: Result of subprocess.call exec Student.py is %s" % result
    if result == FAILURE:
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing Student.py!\n" % container_name)
        sys.exit(1)

    username = getpass.getuser()
    command='docker exec -it %s cat /home/%s/.local/zip.flist' % (container_name, container_user)
#   print "Command to execute is (%s)" % command
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    orig_zipfilenameext = child.stdout.read().strip()
#   print "CreateCopyChownZip: Result of subprocess.Popen exec cat zip.flist is %s" % orig_zipfilenameext
    if orig_zipfilenameext == None:
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing cat zip.flist!\n" % container_name)
        sys.exit(1)

    # The zip filename created by Student.py has the format of e-mail.labname.zip
    orig_zipfilename, orig_zipext = os.path.splitext(orig_zipfilenameext)
    baseZipFilename = os.path.basename(orig_zipfilename)
    #NOTE: Use the '=' to separate e-mail+lab_name from the container_name
    DestZipFilename = '%s=%s.zip' % (baseZipFilename, container_name)
    command = "docker cp %s:%s /home/%s/%s/%s" % (container_name, orig_zipfilenameext, username, host_home_xfer, DestZipFilename)
#   print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CreateCopyChownZip: Result of subprocess.Popen exec cp zip file is %s" % result
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing cp zip file!\n" % container_name)
        sys.exit(1)

    # Change ownership to defined user $USER
    command = "sudo chown %s:%s /home/%s/%s/*.zip" % (username, username, username, host_home_xfer)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CreateCopyChownZip: Result of subprocess.Popen exec chown zip file is %s" % result
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing chown zip file!\n" % container_name)
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
            sys.stderr.write("ERROR: DoStopMultiple Container %s does not exist!\n" % mycontainer_name)
        else:
            # Before stopping a container, run 'Student.py'
            # This will create zip file of the result
            CreateCopyChownZip(mycwd, start_config, mycontainer_name, mycontainer_image, container_user)
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
   
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, "student")

    # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
    host_xfer_dir = '%s/%s' % (myhomedir, start_config.host_home_xfer)
    CreateHostHomeXfer(host_xfer_dir)

    DoStop(start_config, mycwd, labname)

    # Inform user where results are stored
    print "Results stored in directory: %s" % host_xfer_dir

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

