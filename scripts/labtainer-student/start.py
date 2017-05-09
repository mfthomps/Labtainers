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

# Filename: start.py
# Description:
# This is the start script to be run by the student.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#

# Usage: start.py <labname>
# Arguments:
#    <labname> - the lab to start
def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: start.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname)
    labutils.logger.INFO("Begin logging start.py for %s lab" % labname)
    labutils.StartLab(labname, "student", False)

    return 0

if __name__ == '__main__':
    sys.exit(main())

