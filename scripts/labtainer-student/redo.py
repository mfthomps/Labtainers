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

# Filename: redo.py
# Description:
# For lab development testing workflow.  This will stop containers of a lab, create or update lab images
# and start the containers.
#

import sys
import labutils
import logging
import LabtainerLogging

# Usage: redo.py <labname>
# Arguments:
#    <labname> - the lab to stop, delete and start
def main():
    if len(sys.argv) < 2 or len(sys.argv)>3:
        sys.stderr.write("Usage: redo.py <labname> [-f]\n")
        sys.stderr.write("   -f will force a rebuild.\n")
        sys.exit(1)
    force_build = False
    if len(sys.argv) == 3 and sys.argv[2] == '-f':
        force_build = True 
    labname = sys.argv[1]
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname)
    labutils.logger.INFO("Begin logging redo.py for %s lab" % labname)
    labutils.RedoLab(labname, "student", force_build=force_build)

    return 0

if __name__ == '__main__':
    sys.exit(main())

