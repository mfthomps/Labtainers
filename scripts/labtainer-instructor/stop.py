#!/usr/bin/env python

# Filename: stop.py
# Description:
# This is the stop script to be run by the instructor.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#

import getpass
import re
import subprocess
import zipfile

import sys
import os
instructor_cwd = os.getcwd()
student_cwd = instructor_cwd.replace('labtainer-instructor', 'labtainer-student')
print "Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd)
# Append Student CWD to sys.path
sys.path.append(student_cwd)
import labutils

# Usage: stop.py <labname>
# Arguments:
#    <labname> - the lab to stop
def main():
    #print "stop.py -- main"
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: stop.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    labutils.StopLab(labname, "instructor")

    return 0

if __name__ == '__main__':
    sys.exit(main())

