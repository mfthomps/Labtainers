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
import Grader
import AnswerParser
import GoalsParser
import ResultParser

UBUNTUHOME="/home/ubuntu"

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

    studentjsonfname = '%s/.local/config/%s' % (UBUNTUHOME, "studentlab.json")
    studentconfigjson = open(studentjsonfname, "r")
    studentconfig = json.load(studentconfigjson)
    studentconfigjson.close()
    instructorjsonfname = '%s/.local/config/%s' % (UBUNTUHOME, "instructorlab.json")
    instructorconfigjson = open(instructorjsonfname, "r")
    instructorconfig = json.load(instructorconfigjson)
    instructorconfigjson.close()

    # Output grades.txt
    gradesfilename = '%s/%s' % (UBUNTUHOME, "grades.txt")
    gradesfile = open(gradesfilename, "w")
    gradesfile.write("\n")
    #print "Student JSON config is"
    #print studentconfig
    StudentName = studentconfig['studentname']
    StudentHomeDir = studentconfig['studenthomedir']
    LabName = studentconfig['labname']
    LabIDName = studentconfig['labid']
    InstructorName = instructorconfig['instructorname']
    InstructorHomeDir = instructorconfig['instructorhomedir']
    InstructorBaseDir = instructorconfig['instructorbasedir']
    NumStudent = int(instructorconfig['numstudent'])
    GraderScript = instructorconfig['graderscript']

    # Call AnswerParser script to parse 'answer'
    AnswerParser.ParseAnswer()

    index=0
    while index < NumStudent:
        #print "Current index is %d" % index
        index = index + 1

        ZipFileName = 'student%d.%s.zip' % (index, LabIDName)
        DestinationDirName = 'student%d.%s' % (index, LabIDName)
        OutputName = '%s%s' % (InstructorHomeDir, ZipFileName)
        DestDirName = '%s%s' % (InstructorHomeDir, DestinationDirName)
        InstDirName = '%s%s' % (InstructorBaseDir, DestinationDirName)

        #print "Current ZipFilename is %s" % ZipFileName
        #print "Current DestinationDirName is %s" % DestinationDirName
        #print "Current DestDirName is %s" % DestDirName
        #print "Current InstDirName is %s" % InstDirName

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

        # GoalsParser is now tied per student - do this after unzipping file
        # Call GoalsParser script to parse 'goals'
        GoalsParser.ParseGoals(DestDirName)

        # Call ResultParser script to parse students' result
        #command = 'ResultParser.py %s %s %s' % (DestDirName, InstDirName, LabIDName)
        #print "About to do (%s)" % command
        #os.popen(command)
        ResultParser.ParseStdinStdout(DestDirName, InstDirName, LabIDName)

        # Call grader script 
        #command = '%s %s %s %s' % (GraderScript, DestDirName, InstDirName, LabIDName)
        #print "About to do (%s)" % command
        #grades = os.popen(command).read().splitlines()
        grades = Grader.ProcessStudentLab(DestDirName, InstDirName, LabIDName)
        #print "After ProcessStudentLab Instructor, grades is "
        #print grades

        LabIDStudentName = '%s : student%d : ' % (LabIDName, index)
        printresult(gradesfile, LabIDStudentName, grades)

    gradesfile.write("\n")
    gradesfile.close()

    # Inform user where the 'grades.txt' are created
    print "Grades are stored in '%s'" % gradesfilename
    return 0

if __name__ == '__main__':
    sys.exit(main())

