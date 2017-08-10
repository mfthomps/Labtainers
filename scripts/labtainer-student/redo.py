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

# Usage: redo.py <labname> [-f]
# Arguments:
#    <labname> - the lab to stop, delete and start
#    [-f] will force a rebuild
#    [-q] will load the lab using a predetermined email.
def main():
    if len(sys.argv) < 2 or len(sys.argv)>4:
        sys.stderr.write("Usage: redo.py <labname> [-f] [-q]\n")
        sys.stderr.write("   -f will force a rebuild.\n")
        sys.stderr.write("   -q will load the lab using a predetermined email.\n")
        sys.exit(1)
   
    force_build = False
    quiet_build = False
    #if arguments is: redo.py <labname> [-f]
    if len(sys.argv) == 3 and sys.argv[2] == '-f':
        force_build = True 
    #if arguments is: redo.py <labname> [-q]    
    elif len(sys.argv) == 3 and sys.argv[2] == '-q':
        quiet_build = True
    #if arguments is: redo.py <labname> [-q] [-f]    
    elif len(sys.argv) == 4 and sys.argv[2] == '-q' and sys.argv[3] == '-f':
        quiet_build = True
        force_build = True 
    #if arguments is: redo.py <labname> [-f] [-q]    
    elif len(sys.argv) == 4 and sys.argv[2] == '-f' and sys.argv[3] == '-q':
        quiet_build = True
        force_build = True 

    labname = sys.argv[1]
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname)
    labutils.logger.INFO("Begin logging redo.py for %s lab" % labname)
    labutils.RedoLab(labname, "student", force_build=force_build, quiet_build=quiet_build)

    return 0

if __name__ == '__main__':
    sys.exit(main())

