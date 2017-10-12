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

# Instructor.py
# Description: * Read instructorlab.json and extract a zip file
#                containing the student lab work
#              * Call script to grade the student lab work

import copy
import json
import os
import sys
import zipfile
import time
import glob
import GenReport
import Grader
import GoalsParser
import ResultParser
import InstructorLogging

MYHOME=os.getcwd()
logger = InstructorLogging.InstructorLogging("/tmp/instructor.log")
def store_student_parameter(gradesjson, email_labname, student_parameter):
    #print('store_student_parameter email_labname %s student_parameter %s' % (email_labname, student_parameter))
    logger.DEBUG('store_student_parameter email_labname %s student_parameter %s' % (email_labname, student_parameter))
    if email_labname not in gradesjson:
        gradesjson[email_labname] = {}
        gradesjson[email_labname]['parameter'] = copy.deepcopy(student_parameter)
        gradesjson[email_labname]['grades'] = {}
    else:
        if gradesjson[email_labname]['parameter'] != {}:
            # Already have that student's parameter stored
            print("instructor.py store_student_parameter: duplicate email_labname %s student_parameter %s" % (email_labname, student_parameter))
            logger.ERROR("instructor.py store_student_parameter: duplicate email_labname %s student_parameter %s" % (email_labname, student_parameter))
            exit(1)
        else:
            gradesjson[email_labname]['parameter'] = copy.deepcopy(student_parameter)

def store_student_grades(gradesjson, email_labname, grades):
    #print('store_student_grades email_labname %s grades %s' % (email_labname, grades))
    if email_labname not in gradesjson:
        gradesjson[email_labname] = {}
        gradesjson[email_labname]['parameter'] = {}
        gradesjson[email_labname]['grades'] = copy.deepcopy(grades)
    else:
        if gradesjson[email_labname]['grades'] != {}:
            # Already have that student's grades stored
            print("instructor.py store_student_grades: duplicate email_labname %s grades %s" % (email_labname, grades))
            exit(1)
        else:
            gradesjson[email_labname]['grades'] = copy.deepcopy(grades)

# Usage: Instructor.py
# Arguments: None
def main():
    #print "Running Instructor.py"

    logger.INFO("Begin logging instructor.py")

    if len(sys.argv) == 1:
        lab_name_dir = os.path.join(MYHOME,'.local','.labname')
        if not os.path.isfile(lab_name_dir):
            print('ERROR: no file at %s, perhaps running instructor script on wrong containers?')
            logger.ERROR('no file at %s, perhaps running instructor script on wrong containers?')
            exit(1)

        with open(lab_name_dir) as fh:
            LabIDName = fh.read().strip()
    else:
        LabIDName = sys.argv[1]

    # is this used?  
    InstructorBaseDir = os.path.join(MYHOME, '.local', 'base')

    ''' dictionary of container lists keyed by student email_labname '''
    student_list = {}
   
    ''' remove zip files in /tmp/labtainer directory '''
    # /tmp/labtainer will be used to store temporary zip files
    TMPDIR = "/tmp/labtainer"
    if os.path.exists(TMPDIR):
        # exists but is not a directory
        if not os.path.isdir(TMPDIR):
            # remove file then create directory
            os.remove(TMPDIR)
            os.makedirs(TMPDIR)
    else:
        # does not exists, create directory
        os.makedirs(TMPDIR)
    for tmpzip in glob.glob("%s/*.zip" % TMPDIR):
        os.remove(tmpzip)
    
    ''' unzip everything ''' 
    ''' First level unzip '''
    zip_files = glob.glob(MYHOME+'/*.zip')
    first_level_zip = []
    for zfile in zip_files:
        ZipFileName = os.path.basename(zfile)
        first_level_zip.append(ZipFileName)
        OutputName = os.path.join(MYHOME, ZipFileName)
        zipoutput = zipfile.ZipFile(OutputName, "r")
        ''' retain dates of student files '''
        for zi in zipoutput.infolist():
            zipoutput.extract(zi, TMPDIR)
            date_time = time.mktime(zi.date_time + (0, 0, -1))
            dest = os.path.join(TMPDIR, zi.filename)
            os.utime(dest, (date_time, date_time))
        zipoutput.close()

    ''' Second level unzip '''
    zip_files = glob.glob(TMPDIR+'/*.zip')
    for zfile in zip_files:
        ZipFileName = os.path.basename(zfile)
        # Skip first level zip files
        if ZipFileName in first_level_zip:
            continue
        #print('zipfile is %s' % ZipFileName)
        DestinationDirName = os.path.splitext(ZipFileName)[0]
        if '=' in DestinationDirName:
            # NOTE: New format has DestinationDirName as:
            #       e-mail+labname '=' containername
            # get email_labname and containername
            email_labname, containername = DestinationDirName.rsplit('=', 1)
            # Replace the '=' to '/'
            DestinationDirName = '%s/%s' % (email_labname, containername)
            #print email_labname
        else:
            # Old format - no containername
            sys.stderr.write("ERROR: Instructor.py old format (no containername) no longer supported!\n")
            return 1
        student_id = email_labname.rsplit('.', 1)[0]
        #print "student_id is %s" % student_id
        logger.DEBUG("student_id is %s" % student_id)
        if email_labname not in student_list:
            student_list[email_labname] = []
        student_list[email_labname].append(containername) 
        #print('append container %s for student %s' % (containername, email_labname))
        logger.DEBUG('append container %s for student %s' % (containername, email_labname))
        OutputName = '%s/%s' % (TMPDIR, ZipFileName)
        LabDirName = os.path.join(MYHOME, email_labname)
        DestDirName = os.path.join(MYHOME, DestinationDirName)
        InstDirName = os.path.join(InstructorBaseDir, DestinationDirName)

        #print "Student Lab list : "
        #print studentslablist

        if os.path.exists(DestDirName):
            #print "Removing %s" % DestDirName
            os.system('rm -rf %s' % DestDirName)

        zipoutput = zipfile.ZipFile(OutputName, "r")
        ''' retain dates of student files '''
        for zi in zipoutput.infolist():
            zipoutput.extract(zi, DestDirName)
            date_time = time.mktime(zi.date_time + (0, 0, -1))
            dest = os.path.join(DestDirName, zi.filename)
            os.utime(dest, (date_time, date_time))

        zipoutput.close()

    # Store grades, goals, etc
    gradesjson = {}

    ''' create per-student goals.json and process results for each student '''
    for email_labname in student_list:
        # GoalsParser is now tied per student - do this after unzipping file
        # Call GoalsParser script to parse 'goals'
        ''' note odd hack, labinstance seed is stored on container, so need to fine one, use first '''
        DestinationDirName = '%s/%s' % (email_labname, student_list[email_labname][0])
        DestDirName =os.path.join(MYHOME, DestinationDirName)
        student_parameter = GoalsParser.ParseGoals(DestDirName, logger)

        # Call ResultParser script to parse students' result
        LabDirName = os.path.join(MYHOME, email_labname)
        #print('call ResultParser for %s %s' % (email_labname, student_list[email_labname]))
        logger.DEBUG('call ResultParser for %s %s' % (email_labname, student_list[email_labname]))
        ResultParser.ParseStdinStdout(LabDirName, student_list[email_labname], InstDirName, LabIDName, logger)

        # Add student's parameter
        store_student_parameter(gradesjson, email_labname, student_parameter)

    ''' assess the results and generate simple report '''
    for email_labname in student_list:
        LabDirName = os.path.join(MYHOME, email_labname)
        grades = Grader.ProcessStudentLab(LabDirName, LabIDName, logger)
        student_id = email_labname.rsplit('.', 1)[0]
        LabIDStudentName = '%s : %s : ' % (LabIDName, student_id)

        # Add student's grades
        store_student_grades(gradesjson, email_labname, grades)

    #print "grades (in JSON) is "
    #print gradesjson

    # Output <labname>.grades.json
    gradesjsonname = os.path.join(MYHOME, "%s.grades.json" % LabIDName)
    gradesjsonoutput = open(gradesjsonname, "w")
    try:
        jsondumpsoutput = json.dumps(gradesjson, indent=4)
    except:
        print('json dumps failed on %s' % gradesjson)
        exit(1)
    #print('dumping %s' % str(jsondumpsoutput))
    gradesjsonoutput.write(jsondumpsoutput)
    gradesjsonoutput.write('\n')
    gradesjsonoutput.close()

    # Output <labname>.grades.txt
    gradestxtname = os.path.join(MYHOME, "%s.grades.txt" % LabIDName)
    GenReport.CreateReport(gradesjsonname, gradestxtname)

    # Inform user where the 'grades.txt' are created
    print "Grades are stored in '%s'" % gradestxtname
    return 0

if __name__ == '__main__':
    sys.exit(main())

