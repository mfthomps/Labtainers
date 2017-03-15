#!/usr/bin/env python

# Filename: redo.py
# Description:
# For lab development testing workflow
#

import os
import subprocess
import sys
import ParseStartConfig
import start
import stop

LABS_ROOT = os.path.abspath("../../labs/")

def RedoLab(labname):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, "student")
    stop.StopLab(labname)
    for name, container in start_config.containers.items():
        mycontainer_name       = container.full_name
        cmd = 'docker rm %s' % mycontainer_name
        os.system(cmd)
    start.StartLab(labname)

# Usage: redo.py <labname>
# Arguments:
#    <labname> - the lab to stop, delete and start
def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: redo.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    RedoLab(labname)

    return 0

if __name__ == '__main__':
    sys.exit(main())

