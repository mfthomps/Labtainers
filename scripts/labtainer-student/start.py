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
import sys
import labutils
import logging
import LabtainerLogging
import os

# Filename: start.py
# Description:
# This is the start script to be run by the student.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#

# Usage: start.py <labname> [-q]
# Arguments:
#    <labname> - the lab to start
#    [-q] will load the lab using a predetermined email.
def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        sys.stderr.write("Usage: start.py <labname> [-q]\n")
        sys.stderr.write("   -q will load the lab using a predetermined email.\n")
#	tell user list of lesson/folder names in "/labtainer/trunk/labs/"
	sys.stderr.write("List of available labs:\n\n")
	dir_path = os.path.dirname(os.path.realpath(__file__))
	dir_path = dir_path[:dir_path.index("scripts/labtainer-student")]	
	path = dir_path + "labs/"
	dirs = os.listdir(path)
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
    
    quiet_start = False
    if len(sys.argv) == 3 and sys.argv[2] == '-q':
        quiet_start = True
    
    labname = sys.argv[1]
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
    labutils.logger.INFO("Begin logging start.py for %s lab" % labname)
    labutils.StartLab(labname, "student", quiet_start=quiet_start)

    return 0

if __name__ == '__main__':
    sys.exit(main())

