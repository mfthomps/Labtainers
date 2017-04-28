#!/usr/bin/env python

# Instructor.py
# Description: * Read instructorlab.json and extract a zip file
#                containing the student lab work
#              * Call script to grade the student lab work

import json
import os
import sys
import zipfile
import time
import glob
import Grader
import GoalsParser
import ResultParser

UBUNTUHOME="/home/ubuntu"

def store_student_parameter(storejson, email_labname, student_parameter):
    #print('store_student_parameter email_labname %s student_parameter %s' % (email_labname, student_parameter))
    if email_labname not in storejson:
        storejson[email_labname] = {}
        storejson[email_labname]['parameter'] = student_parameter
        storejson[email_labname]['grades'] = {}
    else:
        if storejson[email_labname]['parameter'] != {}:
            # Already have that student's parameter stored
            print("instructor.py store_student_parameter: duplicate email_labname %s student_parameter %s" % (email_labname, student_parameter))
            exit(1)
        else:
            storejson[email_labname]['parameter'] = student_parameter

def store_student_grades(storejson, email_labname, grades):
    #print('store_student_grades email_labname %s grades %s' % (email_labname, grades))
    if email_labname not in storejson:
        storejson[email_labname] = {}
        storejson[email_labname]['parameter'] = {}
        storejson[email_labname]['grades'] = grades
    else:
        if storejson[email_labname]['grades'] != {}:
            # Already have that student's grades stored
            print("instructor.py store_student_grades: duplicate email_labname %s grades %s" % (email_labname, grades))
            exit(1)
        else:
            storejson[email_labname]['grades'] = grades

def printresult(gradesfile, LabIDStudentName, grades):
    gradesfile.write("%s" % LabIDStudentName)
    for (each_key, each_value) in grades.iteritems():
        #print "Current key is ", each_key
        #print "Current value is ", each_value
        if each_key.startswith('_'):
            # Skip, i.e., do not print if it starts with '_'
            continue
        else:
            if each_value:
                gradestring = '%s=%s' % (each_key, "P")
            else:
                gradestring = '%s=%s' % (each_key, "F")
            gradesfile.write('%s ' % gradestring)
    gradesfile.write('\n')

# Usage: Instructor.py
# Arguments: None
def main():
    #print "Running Instructor.py"
    if len(sys.argv) != 1:
        sys.stderr.write("Usage: Instructor.py\n")
        return 1

    instructorjsonfname = '%s/.local/instr_config/%s' % (UBUNTUHOME, "instructorlab.json")
    instructorconfigjson = open(instructorjsonfname, "r")
    instructorconfig = json.load(instructorconfigjson)
    instructorconfigjson.close()

    StudentHomeDir = '/home/ubuntu'
    lab_name_dir = '/home/ubuntu/.local/.labname'
    if not os.path.isfile(lab_name_dir):
        print('ERROR: no file at %s, perhaps running instructor script on wrong containers?')
        exit(1)

    with open(lab_name_dir) as fh:
        LabIDName = fh.read().strip()

    # Output <labname>.grades.txt
    gradesfilename = '%s/%s.%s' % (UBUNTUHOME, LabIDName, "grades.txt")
    gradesfile = open(gradesfilename, "w")
    gradesfile.write("\n")

    InstructorName = instructorconfig['instructorname']
    InstructorHomeDir = instructorconfig['instructorhomedir']
    InstructorBaseDir = instructorconfig['instructorbasedir']
    GraderScript = instructorconfig['graderscript']

    ''' dictionary of container lists keyed by student email_labname '''
    student_list = {}
   
    ''' unzip everything ''' 
    zip_files = glob.glob(InstructorHomeDir+'/*.zip')
    for zfile in zip_files:
        ZipFileName = os.path.basename(zfile)
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
        if email_labname not in student_list:
            student_list[email_labname] = []
        student_list[email_labname].append(containername) 
        #print('append container %s for student %s' % (containername, email_labname))
        OutputName = '%s%s' % (InstructorHomeDir, ZipFileName)
        LabDirName = '%s%s' % (InstructorHomeDir, email_labname)
        DestDirName = '%s%s' % (InstructorHomeDir, DestinationDirName)
        InstDirName = '%s%s' % (InstructorBaseDir, DestinationDirName)

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
    storejson = {}

    ''' create per-student goals.json and process results for each student '''
    for email_labname in student_list:
        # GoalsParser is now tied per student - do this after unzipping file
        # Call GoalsParser script to parse 'goals'
        ''' note odd hack, labinstance seed is stored on container, so need to fine one, use first '''
        DestinationDirName = '%s/%s' % (email_labname, student_list[email_labname][0])
        DestDirName = '%s%s' % (InstructorHomeDir, DestinationDirName)
        student_parameter = GoalsParser.ParseGoals(DestDirName)

        # Call ResultParser script to parse students' result
        LabDirName = '%s%s' % (InstructorHomeDir, email_labname)
        #print('call ResultParser for %s %s' % (email_labname, student_list[email_labname]))
        ResultParser.ParseStdinStdout(LabDirName, student_list[email_labname], InstDirName, LabIDName)

        # Add student's parameter
        store_student_parameter(storejson, email_labname, student_parameter)

    ''' assess the results and generate simple report '''
    for email_labname in student_list:
        LabDirName = '%s%s' % (InstructorHomeDir, email_labname)
        grades = Grader.ProcessStudentLab(LabDirName, LabIDName)
        student_id = email_labname.rsplit('.', 1)[0]
        LabIDStudentName = '%s : %s : ' % (LabIDName, student_id)
        printresult(gradesfile, LabIDStudentName, grades)

        # Add student's grades
        store_student_grades(storejson, email_labname, grades)

    gradesfile.write("\n")
    gradesfile.close()

    #print "store is "
    #print storejson

    # Output <labname>.store.json
    storejsonname = '%s/%s.%s' % (UBUNTUHOME, LabIDName, "store.json")
    storejsonoutput = open(storejsonname, "w")
    try:
        jsondumpsoutput = json.dumps(storejson, indent=4)
    except:
        print('json dumps failed on %s' % storejson)
        exit(1)
    #print('dumping %s' % str(jsondumpsoutput))
    storejsonoutput.write(jsondumpsoutput)
    storejsonoutput.write('\n')
    storejsonoutput.close()

    # Inform user where the 'grades.txt' are created
    print "Grades are stored in '%s'" % gradesfilename
    return 0

if __name__ == '__main__':
    sys.exit(main())

