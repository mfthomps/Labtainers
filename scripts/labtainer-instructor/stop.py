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
# Append Student CWD to sys.path
sys.path.append(student_cwd)
import labutils
import logging
import LabtainerLogging

# Usage: stop.py <labname>
# Arguments:
#    <labname> - the lab to stop
def main():
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", logging.INFO, "labtainerlog")
    labutils.logger.DEBUG("Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd))

    if len(sys.argv) != 2:
        labutils.logger.ERROR("Usage: stop.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    labutils.StopLab(labname, "instructor")

    return 0

if __name__ == '__main__':
    sys.exit(main())

