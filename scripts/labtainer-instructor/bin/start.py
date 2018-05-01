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
import os
import sys
import argparse
import pydoc
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
    dir_path = dir_path[:dir_path.index("scripts/labtainer-instructor")]	
    path = dir_path + "labs/"
    dirs = os.listdir(path)
    parser = argparse.ArgumentParser(description='Start a Labtainers lab.  Provide no arguments see a list of labs.')
    parser.add_argument('labname', help='The lab to run')
    parser.add_argument('-r', '--redo', action='store_true', help='Creates new instance of the lab, previous work will be lost.')
    parser.add_argument('-a', '--all_containers', action='store_true', help='Create all containers as seen by the student.')
    parser.add_argument('-d', '--debug_grade', action='store_true', help='Create the grading container leave it running with a terminal')
    parser.add_argument('-q', '--quiet', action='store_true', help='Do not display results.')
    num_args = len(sys.argv)
    if num_args < 2: 
        showLabs(dirs, path)
        exit(0)
    args = parser.parse_args()
    labname = args.labname
    if labname not in dirs:
        sys.stderr.write("ERROR: Lab named %s was not found!\n" % labname)
        sys.exit(1)

    saki.checkBulkSaki(bulk_path=None, lab=labname)
    lab_path = os.path.join(os.path.abspath('../../labs'), labname)
    if args.quiet or args.all_containers:
        summary = docgoals.getGoalInfo(os.path.join(lab_path,'instr_config'))
        print summary
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
    labutils.logger.INFO("Begin logging start.py for %s lab" % labname)
    auto_grade = True
    if args.all_containers:
        if args.debug_grade:
            print('--all_containers and --debug_grade are mutually exclusive')
            parser.usage()
            exit(1)
        auto_grade = False
    if not args.redo:
        labutils.StartLab(lab_path, "instructor", auto_grade=auto_grade, debug_grade=args.debug_grade, quiet_start=args.quiet)
    else:
        labutils.RedoLab(lab_path, "instructor", force_build=force_build, auto_grade=auto_grade, debug_grade=args.debug_grade, quiet_start=args.quiet)

    return 0
if __name__ == '__main__':
    sys.exit(main())

