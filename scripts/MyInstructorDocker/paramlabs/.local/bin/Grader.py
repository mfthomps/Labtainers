#!/usr/bin/env python

# Grader.py
# Description: Read instructorlab.json and grade the student lab work

import filecmp
import json
import glob
import os
import sys

UBUNTUHOME="/home/ubuntu/"
dirlist = []
matchanylist = []
matchlastlist = []

def processMatchAnyAny(outjsonfnames, grades, goals, answer, eachgoal):
    #print "Inside processMatchAnyAny"
    found = False
    goalid = eachgoal['goalid']
    #print goalid
    tag1 = eachgoal['tag1']
    #print tag1
    tag2 = eachgoal['tag2']
    #print tag2
    #print answer
    #print answer[tag1]

    # Match Any to Any - Process each file until match or not found
    for outputjsonfile in outjsonfnames:
        #print "Output json %s" % outputjsonfile
        jsonfile = open(outputjsonfile, "r")
        jsonoutput = json.load(jsonfile)
        jsonfile.close()

        tag2result = jsonoutput[tag2]
        #print tag2result
        for eachanswer in answer[tag1]:
            current_answer = eachanswer.strip()
            #print "Correct answer is (%s)" % current_answer
            # Since it is match any any - return if match
            if tag2result == current_answer:
               #print "tag2result is (%s) matches answer (%s)" % (tag2result, current_answer)
               found = True
               grades.append("%s=%s" % (goalid, "P"))
               return
 
    # All file processed - still not found
    if not found:
        #print "processMatchAnyAny failed"
        grades.append("%s=%s" % (goalid, "F"))

def processMatchOneAny(outjsonfnames, grades, goals, answer, eachgoal):
    #print "Inside processMatchOneAny"
    found = False
    goalid = eachgoal['goalid']
    #print goalid
    tag1 = eachgoal['tag1']
    #print tag1
    tag2 = eachgoal['tag2']
    #print tag2
    #print answer
    #print answer[tag1]
    answerlen = len(answer[tag1])
    #print "length of answer is (%d)" % answerlen
    if answerlen != 1:
        sys.stdout.write("processMatchOneAny has more than one answer for\n")
        sys.stdout.write("tag1 (%s) = (%s)\n" % (tag1, answer[tag1]))
        sys.exit(1)

    # Match One to Any - Process each file until match or not found
    for outputjsonfile in outjsonfnames:
        #print "Output json %s" % outputjsonfile
        jsonfile = open(outputjsonfile, "r")
        jsonoutput = json.load(jsonfile)
        jsonfile.close()

        tag2result = jsonoutput[tag2]
        #print tag2result
        # Should only have one answer in answer[tag1] because
        # of check above already
        eachanswer = answer[tag1]
        current_answer = eachanswer[0].strip()
        #print "Correct answer is (%s)" % current_answer
        # Since it is match one any - return if match
        if tag2result == current_answer:
           #print "tag2result is (%s) matches answer (%s)" % (tag2result, current_answer)
           found = True
           grades.append("%s=%s" % (goalid, "P"))
           return
 
    # All file processed - still not found
    if not found:
        #print "processMatchOneAny failed"
        grades.append("%s=%s" % (goalid, "F"))

def processMatchOneLast(outjsonfnames, grades, goals, answer, eachgoal):
    #print "Inside processMatchOneLast"
    found = False
    goalid = eachgoal['goalid']
    #print goalid
    tag1 = eachgoal['tag1']
    #print tag1
    tag2 = eachgoal['tag2']
    #print tag2
    #print answer
    #print answer[tag1]
    answerlen = len(answer[tag1])
    #print "length of answer is (%d)" % answerlen
    if answerlen != 1:
        sys.stdout.write("processMatchOneAny has more than one answer for\n")
        sys.stdout.write("tag1 (%s) = (%s)\n" % (tag1, answer[tag1]))
        sys.exit(1)

    # Match One to Last - Process only the last timestamp file
    # until match or not found
    sorted_fnames = sorted(outjsonfnames, reverse=True)
    outputjsonfile = sorted_fnames[0]
    #print "Last file timestamped is (%s)" % outputjsonfile
    #print "Output json %s" % outputjsonfile
    jsonfile = open(outputjsonfile, "r")
    jsonoutput = json.load(jsonfile)
    jsonfile.close()

    tag2result = jsonoutput[tag2]
    #print tag2result
    # Should only have one answer in answer[tag1] because
    # of check above already
    eachanswer = answer[tag1]
    current_answer = eachanswer[0].strip()
    #print "Correct answer is (%s)" % current_answer
    # Since it is match one any - return if match
    if tag2result == current_answer:
        #print "tag2result is (%s) matches answer (%s)" % (tag2result, current_answer)
        found = True
        grades.append("%s=%s" % (goalid, "P"))
        return
 
    # All file processed - still not found
    if not found:
        #print "processMatchOneLast failed"
        grades.append("%s=%s" % (goalid, "F"))


# Process Lab Exercise
def processLabExercise(studentdir, labidname, grades, goals, answer):
    #print "Goals JSON config is"
    #print goals
    #print "Answer JSON config is"
    #print answer
    #for eachgoal in goals:
    #    print "Current goal is "
    #    print eachgoal
    #    print "    goalid is (%s)" % eachgoal['goalid']
    #    print "    goaltype is (%s)" % eachgoal['goaltype']
    #    print "    tag1 is (%s)" % eachgoal['tag1']
    #    print "    tag2 is (%s)" % eachgoal['tag2']
    #    print ""
    #for (each_key, each_value) in answer.iteritems():
    #    print "Current key is ", each_key
    #    print "Current value is ", each_value

    RESULTHOME = '%s/%s' % (studentdir, "result/")
    outjsonfnames = glob.glob('%s/%s.*' % (RESULTHOME, labidname))
    #print outjsonfnames

    # Go through each goal for each student
    for eachgoal in goals:
        if eachgoal['goaltype'] == "matchanyany":
            processMatchAnyAny(outjsonfnames, grades, goals, answer, eachgoal)
        elif eachgoal['goaltype'] == "matchoneany":
            processMatchOneAny(outjsonfnames, grades, goals, answer, eachgoal)
        elif eachgoal['goaltype'] == "matchonelast":
            processMatchOneLast(outjsonfnames, grades, goals, answer, eachgoal)
        else:
            sys.stdout.write("Error: Invalid goal type!\n")
            sys.exit(1)

    return 0

# Usage: ProcessStudentLab <studentdir> <instructordir> <labidname>
# Arguments:
#     <studentdir> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
#     <instructordir> - directory containing instructor's solution
#                       for corresponding student
#     <labidname> - labidname should represent filename of output json file
def ProcessStudentLab(studentdir, instructordir, labidname):
    grades = []
    studentjsonfname = '%s/.local/config/%s' % (UBUNTUHOME, "studentlab.json")
    studentconfigjson = open(studentjsonfname, "r")
    studentconfig = json.load(studentconfigjson)
    studentconfigjson.close()
    #print "Student JSON config is"
    #print studentconfig
    instructorjsonfname = '%s/.local/config/%s' % (UBUNTUHOME, "instructorlab.json")
    instructorconfigjson = open(instructorjsonfname, "r")
    instructorconfig = json.load(instructorconfigjson)
    instructorconfigjson.close()
    #print "Instructor JSON config is"
    #print instructorconfig
    goalsjsonfname = '%s/.local/config/%s' % (UBUNTUHOME, "goals.json")
    goalsjson = open(goalsjsonfname, "r")
    goals = json.load(goalsjson)
    goalsjson.close()
    #print "Goals JSON config is"
    #print goals
    answerjsonfname = '%s/.local/config/%s' % (UBUNTUHOME, "answer.json")
    answerjson = open(answerjsonfname, "r")
    answer = json.load(answerjson)
    answerjson.close()
    #print "Answer JSON config is"
    #print answer

    StudentName = studentconfig['studentname']
    StudentHomeDir = studentconfig['studenthomedir']
    StudentID = studentconfig['studentid']
    LabName = studentconfig['labname']
    LabIDName = studentconfig['labid']
    SaveDirName = studentconfig['savedirectory']
    InstructorName = instructorconfig['instructorname']
    InstructorHomeDir = instructorconfig['instructorhomedir']
    InstructorBaseDir = instructorconfig['instructorbasedir']
    NumStudent = int(instructorconfig['numstudent'])
    GraderScript = instructorconfig['graderscript']

    for dirname in SaveDirName:
        if dirname == 'result':
            #sys.stdout.write('%s = ' % dirname)
            processLabExercise(studentdir, labidname, grades, goals, answer)
            #sys.stdout.write('\n')
    return grades

# Usage: Grader.py <studentdir> <instructordir> <labidname>
# Arguments:
#     <studentdir> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
#     <instructordir> - directory containing instructor's solution
#                       for corresponding student
#     <labidname> - labidname should represent filename of output json file
def main():
    #print "Running Grader.py"
    if len(sys.argv) != 4:
        sys.stderr.write("Usage: Grader.py <studentdir> <instructordir> <labidname>\n")
        return 1

    studentdir = sys.argv[1]
    instructordir = sys.argv[2]
    labidname = sys.argv[3]
    #print "Inside main, grades is "
    #print grades

    ProcessStudentLab(studentdir, instructordir, labidname)

if __name__ == '__main__':
    sys.exit(main())

