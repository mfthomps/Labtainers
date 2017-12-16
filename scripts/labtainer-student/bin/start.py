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
import pydoc
import platform

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
#    [-q] will load the lab using a previously supplied email.
def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path[:dir_path.index("scripts/labtainer-student")]	
    path = dir_path + "labs/"
    dirs = os.listdir(path)
    num_args = len(sys.argv)
    if num_args < 2 or num_args > 3:
        description = ''
        description += "Usage: start.py <labname> [-q]\n"
        description +="   -q will load the lab using a previously supplied email.\n"
#	tell user list of lesson/folder names in "/labtainer/trunk/labs/"
	description+="List of available labs:\n\n"
	for loc in sorted(dirs):
                description = description+'\n  '+loc
		aboutFile = path + loc + "/config/about.txt"
		if(os.path.isfile(aboutFile)):
                    description += ' - '
		    with open(aboutFile) as fh:
		        for line in fh:
                            description += line
                else:
                    description += "\n"
        #sys.stderr.write(description)
        pydoc.pager(description)
        sys.exit(1)
    
    labname = sys.argv[1]
    if num_args == 2 and labname not in dirs:
        sys.stderr.write("ERROR: Lab named %s was not found!\n" % labname)
        sys.exit(1)

    quiet_start = False
    if num_args == 3 and sys.argv[2] == '-q':
        quiet_start = True
    
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
    labutils.logger.INFO("Begin logging start.py for %s lab" % labname)
    lab_path = os.path.join(os.path.abspath('../../labs'), labname)
    update_flag='../../../.doupdate'
    if os.path.isfile(update_flag):
        ''' for prepackaged VMs, do not auto update after first lab is run '''
        os.remove(update_flag)
    print('lab_path is %s' % lab_path)
    labutils.StartLab(lab_path, "student", quiet_start=quiet_start)

    return 0

if __name__ == '__main__':
    sys.exit(main())

