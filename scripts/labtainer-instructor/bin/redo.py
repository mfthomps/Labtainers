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
import saki
instructor_cwd = os.getcwd()
student_cwd = instructor_cwd.replace('labtainer-instructor', 'labtainer-student')
# Append Student CWD to sys.path
sys.path.append(student_cwd+"/bin")
sys.path.append(os.path.join(instructor_cwd, 'assess_bin'))
import labutils
import logging
import LabtainerLogging
import docgoals

# Usage: redo.py <labname> [-f]
# Arguments:
#    <labname> - the lab to stop, delete and start
#    [-f] will force a rebuild
def main():
    if len(sys.argv) < 2 or len(sys.argv)>3:
        sys.stderr.write("Usage: redo.py <labname> [-f]\n")
        sys.stderr.write("   -f will force a rebuild.\n")
        sys.exit(1)
    force_build = False
    if len(sys.argv) == 3 and sys.argv[2] == '-f':
        force_build = True 
    labname = sys.argv[1]
    saki.checkBulkSaki(bulk_path=None, lab=labname)
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
    labutils.logger.INFO("Begin logging redo.py for %s lab" % labname)
    labutils.logger.DEBUG("Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd))
    lab_path = os.path.join(os.path.abspath('../../labs'), labname)
    summary = docgoals.getGoalInfo(os.path.join(lab_path,'instr_config'))
    print summary
    labutils.RedoLab(lab_path, "instructor", force_build=force_build)

    return 0

if __name__ == '__main__':
    sys.exit(main())

