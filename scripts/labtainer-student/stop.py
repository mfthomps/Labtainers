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
# This is the stop script to be run by the student.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#

import sys
import labutils
import logging
import LabtainerLogging

# Usage: stop.py <labname>
# Arguments:
#    <labname> - the lab to stop
def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: stop.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname)
    labutils.logger.INFO("Begin logging stop.py for %s lab" % labname)
    # Pass 'False' to ignore_stop_error (i.e., do not ignore error)
    labutils.StopLab(labname, "student", False)

    return 0

if __name__ == '__main__':
    sys.exit(main())

