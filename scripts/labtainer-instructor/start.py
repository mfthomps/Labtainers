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
# Append Student CWD to sys.path
sys.path.append(student_cwd)

import ParseStartConfig
import labutils
import logging
import LabtainerLogging

# Usage: start.py <labname>
# Arguments:
#    <labname> - the lab to start
def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: start.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
    labutils.logger.INFO("Begin logging start.py for %s lab" % labname)
    labutils.logger.DEBUG("Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd))
    labutils.StartLab(labname, "instructor")

    return 0

if __name__ == '__main__':
    sys.exit(main())

