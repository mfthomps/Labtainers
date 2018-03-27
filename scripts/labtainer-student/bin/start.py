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
import sys
import labutils
import logging
import LabtainerLogging
import os
import pydoc
import platform
import argparse
import CurrentLab
'''
Start a Labtainers exercise.
'''
def showLabs(dirs, path):
    description = ''
    description += 'Start a Labtainers lab\n'
    description+="List of available labs:\n\n"
    for loc in sorted(dirs):
        description = description+'\n  '+loc
	aboutFile = path + loc + "/config/about.txt"
	if(os.path.isfile(aboutFile)):
            description += ' - '
	    with open(aboutFile) as fh:
	        for line in fh:
                    description += line
        else:
            description += "\n"
            #sys.stderr.write(description)
    pydoc.pager(description)
    print('Use "-h" for help.')

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path[:dir_path.index("scripts/labtainer-student")]	
    path = dir_path + "labs/"
    dirs = os.listdir(path)
    parser = argparse.ArgumentParser(description='Start a Labtainers lab.  Provide no arguments see a list of labs.')
    parser.add_argument('labname', help='The lab to run')
    parser.add_argument('-q', '--quiet', action='store_true', help='Do not prompt for email, use previoulsy supplied email.')
    parser.add_argument('-s', '--servers', action='store_true', help='Intended for distributed Labtainers, start the containers that are not clients.')
    parser.add_argument('-w', '--workstation', action='store_true', help='Intended for distributed Labtainers, start the client workstation.')
    parser.add_argument('-n', '--client_count', action='store', help='Number of clones of client components to create, itended for multi-user labs')
    parser.add_argument('-o', '--only_container', action='store', help='run only the named container')
    num_args = len(sys.argv)
    if num_args < 2: 
        showLabs(dirs, path)
        exit(0)
    args = parser.parse_args()
    labname = args.labname
    if labname not in dirs:
        sys.stderr.write("ERROR: Lab named %s was not found!\n" % labname)
        sys.exit(1)

    
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
    labutils.logger.INFO("Begin logging start.py for %s lab" % labname)
    lab_path = os.path.join(os.path.abspath('../../labs'), labname)
    update_flag='../../../.doupdate'
    if os.path.isfile(update_flag):
        ''' for prepackaged VMs, do not auto update after first lab is run '''
        os.remove(update_flag)
    #print('lab_path is %s' % lab_path)
    distributed = None
    if args.servers and args.workstation:
        print('--server and --workstation are mutually exclusive')
        exit(1)
    elif args.servers: 
        distributed = 'server' 
    elif args.workstation:
        distributed = 'client'
    if distributed is not None and args.client_count is not None:
        print('Cannot specify --server or --client if a --client_count is provided')
        exit(1)
    labutils.StartLab(lab_path, "student", quiet_start=args.quiet, run_container=args.only_container, servers=distributed, clone_count=args.client_count)
    current_lab = CurrentLab.CurrentLab()
    current_lab.add('lab_name', args.labname)
    current_lab.add('clone_count', args.client_count)
    current_lab.add('servers', distributed)
    current_lab.save()

    return 0

if __name__ == '__main__':
    sys.exit(main())

