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
sys.path.append(student_cwd+"/bin")

import labutils
import logging
import LabtainerLogging

# Usage: start.py <labname>
# Arguments:
#    <labname> - the lab to start
def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path[:dir_path.index("scripts/labtainer-instructor")]	
    path = dir_path + "labs/"
    dirs = os.listdir(path)
    num_args = len(sys.argv)
    if num_args < 2 or num_args > 3:
        sys.stderr.write("Usage: start.py <labname> [-q]\n")
        sys.stderr.write("   -q will load the lab using a predetermined email.\n")
#	tell user list of lesson/folder names in "/labtainer/trunk/labs/"
	sys.stderr.write("List of available labs:\n\n")
	for loc in sorted(dirs):
                description = '  '+loc
		aboutFile = path + loc + "/config/about.txt"
		if(os.path.isfile(aboutFile)):
                    description += ' - '
		    with open(aboutFile) as fh:
		        for line in fh:
                            description += line
                else:
                    description += "\n"
                sys.stderr.write(description)
        sys.exit(1)
    labname = sys.argv[1]
    if num_args == 2 and labname not in dirs:
        sys.stderr.write("ERROR: Lab named %s was not found!\n" % labname)
        sys.exit(1)
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
    labutils.logger.INFO("Begin logging start.py for %s lab" % labname)
    labutils.logger.DEBUG("Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd))
    lab_path = os.path.join(os.path.abspath('../../labs'), labname)
    labutils.StartLab(lab_path, "instructor")

    return 0

if __name__ == '__main__':
    sys.exit(main())

