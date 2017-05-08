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

# Filename: regresstest.py
# Description:
# Regression Testing script. This script will make use of labutils.
#
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
import Labtainer
Labtainer.logger.DEBUG("Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd))

def usage():
    Labtainer.logger.ERROR("Usage: regresstest.py [<labname>]\n")
    sys.exit(1)

# Usage: regresstest.py
# Arguments: None
def main():
    Labtainer.logger = LabtainerLogging.LabtainerLogging("labtainer.log", logging.INFO, "labtainerlog")
    labnamelist = []
    num_args = len(sys.argv)
    if num_args == 1:
        Labtainer.logger.DEBUG("LABS_ROOT is %s" % labutils.LABS_ROOT)
        labnamelist = os.listdir(labutils.LABS_ROOT)
    elif num_args == 2:
        labnamelist.append(sys.argv[1])
    else:
        usage()

    for labname in labnamelist:
        Labtainer.logger.DEBUG("Current name is (%s)" % labname)
        fulllabname = os.path.join(labutils.LABS_ROOT, labname)
        if labname == "etc" or labname == "bin":
            Labtainer.logger.DEBUG("skipping etc or bin")
            continue

        if os.path.isdir(fulllabname):
            Labtainer.logger.DEBUG("(%s) is directory - assume (%s) is a labname" % (fulllabname, labname))
    
            # RegressTest will do test following:
            # 1. This will stop containers of a lab, create or update lab images and start the containers.
            # 2. After the containers are started, it will invoke 'instructor.py' on the GRADE_CONTAINER.
            # 3. Stop the containers to obtain the 'grades.txt'
            # 4. Compare 'grades.txt.GOLD' vs. 'grades.txt'
            RegressTestResult = labutils.RegressTest(labname, "instructor")
            if RegressTestResult == False:
                # False means grades.txt.GOLD != grades.txt, output error then break
                print("RegressTest fails on %s lab" % labname)
                sys.exit(1)
            else:
                print("RegressTest on %s lab SUCCESS" % labname)

    return 0

if __name__ == '__main__':
    sys.exit(main())

