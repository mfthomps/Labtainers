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
import os
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
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
    labutils.logger.INFO("Begin logging stop.py for %s lab" % labname)
    # Pass 'False' to ignore_stop_error (i.e., do not ignore error)
    lab_path = os.path.join(os.path.abspath('../../labs'), labname)
    has_running_containers, running_containers_list = labutils.GetRunningContainersList()
    if has_running_containers:
        has_lab_role, labnamelist = labutils.GetRunningLabNames(running_containers_list, "student")
        if has_lab_role:
            if labname not in labnamelist:
                labutils.logger.ERROR("No lab named %s in currently running labs!" % labname)
                sys.exit(1)
        else:
            labutils.logger.ERROR("No running labs in student's role")
            sys.exit(1)
    else:
        labutils.logger.ERROR("No running labs at all")
        sys.exit(1)
    labutils.StopLab(lab_path, "student", False)

    return 0

if __name__ == '__main__':
    sys.exit(main())

