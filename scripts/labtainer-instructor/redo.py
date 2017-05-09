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
import os
instructor_cwd = os.getcwd()
student_cwd = instructor_cwd.replace('labtainer-instructor', 'labtainer-student')
# Append Student CWD to sys.path
sys.path.append(student_cwd)
import labutils
import logging
import LabtainerLogging

# Usage: redo.py <labname>
# Arguments:
#    <labname> - the lab to stop, delete and start
def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: redo.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname)
    labutils.logger.INFO("Begin logging redo.py for %s lab" % labname)
    labutils.logger.DEBUG("Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd))
    labutils.RedoLab(labname, "instructor", False)

    return 0

if __name__ == '__main__':
    sys.exit(main())

