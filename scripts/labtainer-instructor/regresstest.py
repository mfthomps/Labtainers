#!/usr/bin/env python

# Filename: regresstest.py
# Description:
# Regression Testing script. This script will make use of labutils.
#
#

import sys
import os
instructor_cwd = os.getcwd()
student_cwd = instructor_cwd.replace('labtainer-instructor', 'labtainer-student')
#print "Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd)
# Append Student CWD to sys.path
sys.path.append(student_cwd)
import labutils

def usage():
    sys.stderr.write("Usage: regresstest.py [<labname>]\n")
    sys.exit(1)

# Usage: regresstest.py
# Arguments: None
def main():
    labnamelist = []
    num_args = len(sys.argv)
    if num_args == 1:
        #print "LABS_ROOT is %s" % labutils.LABS_ROOT
        labnamelist = os.listdir(labutils.LABS_ROOT)
    elif num_args == 2:
        labnamelist.append(sys.argv[1])
    else:
        usage()

    for labname in labnamelist:
        #print "Current name is (%s)" % labname
        fulllabname = os.path.join(labutils.LABS_ROOT, labname)
        if labname == "etc" or labname == "bin":
            #print "skipping etc or bin"
            continue

        if os.path.isdir(fulllabname):
            print "(%s) is directory - assume (%s) is a labname" % (fulllabname, labname)
    
            # RegressTest will do test following:
            # 0. Copy zip files from testsets directory to transfer directory
            # 1. This will stop containers of a lab, create or update lab images and start the containers.
            # 2. After the containers are started, it will invoke 'instructor.py' on the GRADE_CONTAINER.
            # 3. Stop the containers to obtain the 'grades.txt'
            # 4. Compare 'grades.txt.GOLD' vs. 'grades.txt'
            RegressTestResult = labutils.RegressTest(labname, "instructor")
            if RegressTestResult == False:
                # False means grades.txt.GOLD != grades.txt, print error then break
                print "RegressTest fails on %s lab" % labname
                sys.exit(1)
            else:
                print "RegressTest on %s lab SUCCESS" % labname

    return 0

if __name__ == '__main__':
    sys.exit(main())

