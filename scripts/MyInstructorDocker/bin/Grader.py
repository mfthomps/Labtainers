#!/usr/bin/env python

# Grader.py
# Description: Read instructorlab.json and grade the student lab work

import filecmp
import json
import glob
import os
import sys
import evalBoolean

UBUNTUHOME="/home/ubuntu/"
dirlist = []
matchanylist = []
matchlastlist = []

def compare_result_answer(current_result, current_answer, operator):
    found = False
    if "integer" in operator:
        if current_result.startswith('0x'):
            result_int = int(current_result, 16)
        else:
            result_int = int(current_result, 10)
        if current_answer.startswith('0x'):
            answer_int = int(current_answer, 16)
        else:
            answer_int = int(current_answer, 10)
    if operator == "string_equal":
        if current_result == current_answer:
            found = True
    elif operator == "string_diff":
        if current_result != current_answer:
            found = True
    elif operator == "string_start":
        if current_result.startswith(current_answer):
            found = True
    elif operator == "string_end":
        if current_result.endswith(current_answer):
            found = True
    elif operator == "integer_equal":
        if result_int == answer_int:
            found = True
    elif operator == "integer_greater":
        if result_int > answer_int:
            found = True
    elif operator == "integer_lessthan":
        if result_int < answer_int:
            found = True
    else:
        found = False

    return found

def processMatchAnyAny(outjsonfnames, grades, answer, eachgoal):
    #print "Inside processMatchAnyAny"
    found = False
    goalid = eachgoal['goalid']
    #print goalid
    jsonanswertag = eachgoal['answertag']
    #print jsonanswertag
    jsonresulttag = eachgoal['resulttag']
    (resulttagtarget, resulttag) = jsonresulttag.split('.')
    #print jsonresulttag
    # Handle special case 'answer=<string>'
    one_answer = False
    if '=' in jsonanswertag:
        (answertag, onlyanswer) = jsonanswertag.split('=')
        current_onlyanswer = onlyanswer.strip()
        # Change to one_answer = True
        one_answer = True
        #print "Current onlyanswer is (%s)" % current_onlyanswer
    else:
        # Determine whether to use 'Answer' or 'Result' for answertag
        (use_target, answertagstring) = jsonanswertag.split('.')
        #print use_target
        #print answertagstring

    # Match Any to Any - Process each file until match or not found
    for outputjsonfile in outjsonfnames:
        #print "Output json %s" % outputjsonfile
        jsonfile = open(outputjsonfile, "r")
        jsonoutput = json.load(jsonfile)
        jsonfile.close()
        try:
            resulttagresult = jsonoutput[resulttag]
        except:
            print('%s not found in file %s' % (resulttag, outputjsonfile))
            exit(1)
        #print resulttagresult
        if one_answer:
            found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
            if found:
                #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
                grades[goalid] = True
                return
        else:
            # Compare 'Answer' vs. 'Result'
            if use_target == "answer":
                for eachanswer in answer[answertagstring]:
                    current_answer = eachanswer.strip()
                    #print "Correct answer is (%s)" % current_answer
                    found = compare_result_answer(resulttagresult, current_answer, eachgoal['goaloperator'])
                    if found:
                        #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_answer)
                        grades[goalid] = True
                        return
            # Compare 'Result' vs. 'Result'
            else:
                answertagresult = jsonoutput[answertagstring]
                current_answer = answertagresult.strip()
                #print "Correct answer is (%s)" % current_answer
                found = compare_result_answer(resulttagresult, current_answer, eachgoal['goaloperator'])
                if found:
                    #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_answer)
                    grades[goalid] = True
                    return
 
    # All file processed - still not found
    if not found:
        #print "processMatchAnyAny failed"
        grades[goalid] = False

def processMatchOneAny(outjsonfnames, grades, answer, eachgoal):
    #print "Inside processMatchOneAny"
    found = False
    goalid = eachgoal['goalid']
    #print goalid
    jsonanswertag = eachgoal['answertag']
    #print jsonanswertag
    jsonresulttag = eachgoal['resulttag']
    (resulttagtarget, resulttag) = jsonresulttag.split('.')
    #print jsonresulttag
    # Handle special case 'answer=<string>'
    one_answer = False
    if '=' in jsonanswertag:
        (answertag, onlyanswer) = jsonanswertag.split('=')
        current_onlyanswer = onlyanswer.strip()
        # Change to one_answer = True
        one_answer = True
        #print "Current onlyanswer is (%s)" % current_onlyanswer
    else:
        # Determine whether to use 'Answer' or 'Result' for answertag
        (use_target, answertagstring) = jsonanswertag.split('.')
        #print use_target
        #print answertagstring

    # Match One to Any - Process each file until match or not found
    for outputjsonfile in outjsonfnames:
        #print "Output json %s" % outputjsonfile
        jsonfile = open(outputjsonfile, "r")
        jsonoutput = json.load(jsonfile)
        jsonfile.close()

        resulttagresult = jsonoutput[resulttag]
        #print resulttagresult
        if one_answer:
            found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
            if found:
                #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
                grades[goalid] = True
                return
        else:
            # Compare 'Answer' vs. 'Result'
            if use_target == "answer":
                answerlen = len(answer[answertagstring])
                #print "length of answer is (%d)" % answerlen
                if answerlen != 1:
                    sys.stdout.write("processMatchOneAny has more than one answer for\n")
                    sys.stdout.write("answertagstring (%s) = (%s)\n" % (answertagstring, answer[answertagstring]))
                    sys.exit(1)
                #print answer
                #print answer[answertagstring]
                eachanswer = answer[answertagstring]
                current_onlyanswer = eachanswer[0].strip()
            else:
            # Compare 'Result' vs. 'Result'
                current_onlyanswer = jsonoutput[answertagstring]

            #print "Correct onlyanswer is (%s)" % current_onlyanswer

            found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
            if found:
                #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
                grades[goalid] = True
                return
 
    # All file processed - still not found
    if not found:
        #print "processMatchOneAny failed"
        grades[goalid] = False

def processMatchOneLast(outjsonfnames, grades, answer, eachgoal):
    #print "Inside processMatchOneLast"
    found = False
    goalid = eachgoal['goalid']
    #print goalid
    jsonanswertag = eachgoal['answertag']
    #print jsonanswertag
    jsonresulttag = eachgoal['resulttag']
    (resulttagtarget, resulttag) = jsonresulttag.split('.')
    #print jsonresulttag
    # Handle special case 'answer=<string>'
    one_answer = False
    if '=' in jsonanswertag:
        (answertag, onlyanswer) = jsonanswertag.split('=')
        current_onlyanswer = onlyanswer.strip()
        # Change to one_answer = True
        one_answer = True
        #print "Current onlyanswer is (%s)" % current_onlyanswer
    else:
        # Determine whether to use 'Answer' or 'Result' for answertag
        (use_target, answertagstring) = jsonanswertag.split('.')
        #print use_target
        #print answertagstring

    # Match One to Last - Process only the last timestamp file
    # until match or not found
    sorted_fnames = sorted(outjsonfnames, reverse=True)
    outputjsonfile = sorted_fnames[0]
    #print "Last file timestamped is (%s)" % outputjsonfile
    #print "Output json %s" % outputjsonfile
    jsonfile = open(outputjsonfile, "r")
    jsonoutput = json.load(jsonfile)
    jsonfile.close()

    resulttagresult = jsonoutput[resulttag]
    #print resulttagresult
    if one_answer:
        found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
        if found:
            #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
            grades[goalid] = True
            return
    else:
        # Compare 'Answer' vs. 'Result'
        if use_target == "answer":
            answerlen = len(answer[answertagstring])
            #print "length of answer is (%d)" % answerlen
            if answerlen != 1:
                sys.stdout.write("processMatchOneAny has more than one answer for\n")
                sys.stdout.write("answertagstring (%s) = (%s)\n" % (answertagstring, answer[answertagstring]))
                sys.exit(1)
            #print answer
            #print answer[answertagstring]
            eachanswer = answer[answertagstring]
            current_onlyanswer = eachanswer[0].strip()
        else:
        # Compare 'Result' vs. 'Result'
            current_onlyanswer = jsonoutput[answertagstring]

        #print "Correct onlyanswer is (%s)" % current_onlyanswer

        found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
        if found:
            #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
            grades[goalid] = True
            return
 
    # All file processed - still not found
    if not found:
        #print "processMatchOneLast failed"
        grades[goalid] = False


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
    #    print "    answertag is (%s)" % eachgoal['answertag']
    #    print "    resulttag is (%s)" % eachgoal['resulttag']
    #    print ""
    #for (each_key, each_value) in answer.iteritems():
    #    print "Current key is ", each_key
    #    print "Current value is ", each_value

    RESULTHOME = '%s/%s' % (studentdir, ".local/result/")
    outjsonfnames = glob.glob('%s/%s.*' % (RESULTHOME, labidname))
    #print outjsonfnames

    # Go through each goal for each student
    # Do the goaltype of non 'boolean' first
    for eachgoal in goals:
        if eachgoal['goaltype'] == "matchanyany":
            processMatchAnyAny(outjsonfnames, grades, answer, eachgoal)
        elif eachgoal['goaltype'] == "matchoneany":
            processMatchOneAny(outjsonfnames, grades, answer, eachgoal)
        elif eachgoal['goaltype'] == "matchonelast":
            processMatchOneLast(outjsonfnames, grades, answer, eachgoal)
        elif eachgoal['goaltype'] == "boolean":
            #print "Skipping %s" % eachgoal
            continue
        else:
            sys.stdout.write("Error: Invalid goal type!\n")
            sys.exit(1)

    # Now do the goaltype of 'boolean'
    for eachgoal in goals:
        if (eachgoal['goaltype'] == "matchanyany" or
            eachgoal['goaltype'] == "matchoneany" or
            eachgoal['goaltype'] == "matchonelast"):
            continue
        elif eachgoal['goaltype'] == "boolean":
            t_string = eachgoal['boolean_string']
            boolean_result = evalBoolean.evaluate_boolean_expression(t_string, grades)
            goalid = eachgoal['goalid']
            grades[goalid] = boolean_result
        else:
            sys.stdout.write("Error: Invalid goal type!\n")
    return 0

# Usage: ProcessStudentLab <studentdir> <instructordir> <labidname>
# Arguments:
#     <studentdir> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
#     <instructordir> - directory containing instructor's solution
#                       for corresponding student
#     <labidname> - labidname should represent filename of output json file
def ProcessStudentLab(studentdir, instructordir, labidname):
    grades = {}
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
    InstructorName = instructorconfig['instructorname']
    InstructorHomeDir = instructorconfig['instructorhomedir']
    InstructorBaseDir = instructorconfig['instructorbasedir']
    NumStudent = int(instructorconfig['numstudent'])
    GraderScript = instructorconfig['graderscript']

    processLabExercise(studentdir, labidname, grades, goals, answer)
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

