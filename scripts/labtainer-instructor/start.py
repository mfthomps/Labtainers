#!/usr/bin/env python

# Filename: start.py
# Description:
# This is the start script to be run by the instructor.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#

import getpass
import glob
import json
import md5
import os
import sys

instructor_cwd = os.getcwd()
student_cwd = instructor_cwd.replace('labtainer-instructor', 'labtainer-student')
print "Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd)
# Append Student CWD to sys.path
sys.path.append(student_cwd)

import ParseStartConfig
import labutils
# Usage: start.py <labname>
# Arguments:
#    <labname> - the lab to start
def main():
    #print "start.py -- main"
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: start.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    labutils.StartLab(labname, "instructor")

    return 0

if __name__ == '__main__':
    sys.exit(main())

