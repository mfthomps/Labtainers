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
import labutils
import logging
import LabtainerLogging
import argparse


# Usage: redo.py <labname> [-f]
# Arguments:
#    <labname> - the lab to stop, delete and start
#    [-f] will force a rebuild
#    [-q] will load the lab using a predetermined email.
def main():
    parser = argparse.ArgumentParser(description='Build the images of a lab')
    parser.add_argument('labname', help='The lab to build')
    parser.add_argument('-f', '--force', action='store_true', help='force build')
    parser.add_argument('-p', '--prompt', action='store_true', help='prompt for email, otherwise use stored')
    parser.add_argument('-c', '--container', action='store', help='force rebuild just this container')

    args = parser.parse_args()
    quiet_start = True
    if args.prompt == True:
        quiet_start = False
    if args.force is not None:
        force_build = args.force
    #print('force %s quiet %s container %s' % (force_build, quiet_start, args.container))
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", args.labname, "../../config/labtainer.config")
    labutils.logger.INFO("Begin logging Rebuild.py for %s lab" % args.labname)
    lab_path = os.path.join(os.path.abspath('../../labs'), args.labname)
    labutils.RebuildLab(lab_path, "student", force_build=force_build, quiet_start=quiet_start, just_container=args.container)

    return 0

if __name__ == '__main__':
    sys.exit(main())

