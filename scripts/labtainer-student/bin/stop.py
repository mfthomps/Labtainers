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

'''
Stop a given Labtainers lab.  If no arguments are given, then all running
labs will be stopped.
'''

import sys
import os
import labutils
import logging
import LabtainerLogging
import CurrentLab
import argparse

# Usage: stop.py <labname>
# Arguments:
#    <labname> - the lab to stop
def main():
    parser = argparse.ArgumentParser(description='Stop a Labtainers lab.  If no arguments are provided, then all labs are stopped.')
    parser.add_argument('lab', nargs='?', default='all')
    args = parser.parse_args()
    
    labname = args.lab
    lablist = []
    if labname != 'all':
        labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
        lablist.append(labname)
    else:
        labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
        lablist = labutils.GetListRunningLab()

    for labname in lablist:
        labutils.logger.info("Begin logging stop.py for %s lab" % labname)
        # Pass 'False' to ignore_stop_error (i.e., do not ignore error)
        lab_path = os.path.join(os.path.abspath('../../labs'), labname)
        has_running_containers, running_containers_list = labutils.GetRunningContainersList()
        if has_running_containers:
            has_lab_role, labnamelist = labutils.GetRunningLabNames(running_containers_list)
            if has_lab_role:
                if labname not in labnamelist:
                    labutils.logger.error("No lab named %s in currently running labs!" % labname)
                    sys.exit(1)
            else:
                labutils.logger.error("Student is not running any labs")
                sys.exit(1)
        else:
            labutils.logger.error("No running labs at all")
            sys.exit(1)
        current_lab = CurrentLab.CurrentLab()
        clone_count = current_lab.get('clone_count')        
        servers = current_lab.get('servers')        
        labutils.StopLab(lab_path, False, servers=servers, clone_count=clone_count)
        current_lab.clear()

    return 0

if __name__ == '__main__':
    sys.exit(main())

