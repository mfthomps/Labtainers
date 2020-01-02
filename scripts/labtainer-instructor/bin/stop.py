#!/usr/bin/env python3
'''
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''

# Filename: stop.py
# Description:
# This is the stop script to be run by the instructor.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#

import getpass
import re
import subprocess
import zipfile

import sys
import os
instructor_cwd = os.getcwd()
student_cwd = instructor_cwd.replace('labtainer-instructor', 'labtainer-student')
# Append Student CWD to sys.path
sys.path.append(student_cwd+"/bin")
import labutils
import logging
import LabtainerLogging

# Usage: stop.py <labname>
# Arguments:
#    <labname> - the lab to stop
def main():
    if len(sys.argv) > 2:
        sys.stderr.write("Usage: stop.py [<labname>]\n")
        sys.exit(1)
    
    lablist = []
    if len(sys.argv) == 2:
        labname = sys.argv[1]
        labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
        lablist.append(labname)
    else:
        labname = "all"
        # labutils.logger need to be set before calling GetListRunningLab()
        labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
        lablist = labutils.GetListRunningLab()

    for labname in lablist:
        labutils.logger.info("Begin logging stop.py for %s lab" % labname)
        labutils.logger.debug("Instructor CWD = (%s), Student CWD = (%s)" % (instructor_cwd, student_cwd))
        # Pass 'False' to ignore_stop_error (i.e., do not ignore error)
        lab_path = os.path.join(os.path.abspath('../../labs'), labname)
        has_running_containers, running_containers_list = labutils.GetRunningContainersList()
        if has_running_containers:
            has_lab_role, labnamelist = labutils.GetRunningLabNames(running_containers_list, "instructor")
            if has_lab_role:
                if labname not in labnamelist:
                    labutils.logger.error("No lab named %s in currently running labs!" % labname)
                    sys.exit(1)
            else:
                labutils.logger.error("No running labs in instructor's role")
                sys.exit(1)
        else:
            labutils.logger.error("No running labs at all")
            sys.exit(1)
        labutils.StopLab(lab_path, "instructor", False)

    return 0

if __name__ == '__main__':
    sys.exit(main())

