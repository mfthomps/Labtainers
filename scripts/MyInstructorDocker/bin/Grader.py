#!/usr/bin/env python

# Grader.py
# Description: Read instructorlab.json and grade the student lab work

import collections
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

def processMatchAnyAny(outjsonfnames, grades, eachgoal):
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
        # No more answer.config (parameter or parameter_ascii will become answer=<value> already)
        (use_target, answertagstring) = jsonanswertag.split('.')
        #print use_target
        #print answertagstring

    # Match Any to Any - Process each file until match or not found
    for outputjsonfile in outjsonfnames:
        #print "processMatchAnyAny Output json %s" % outputjsonfile
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

def processMatchOneAny(outjsonfnames, grades, eachgoal):
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
        # No more answer.config (parameter or parameter_ascii will become answer=<value> already)
        (use_target, answertagstring) = jsonanswertag.split('.')
        #print use_target
        #print answertagstring

    # Match One to Any - Process each file until match or not found
    for outputjsonfile in outjsonfnames:
        #print "processMatchOneAny Output json %s" % outputjsonfile
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

def processMatchOneLast(outjsonfnames, grades, subgoalsresult, eachgoal):
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
        # No more answer.config (parameter or parameter_ascii will become answer=<value> already)
        (use_target, answertagstring) = jsonanswertag.split('.')
        #print use_target
        #print answertagstring

    # Match One to Last - Process only the last timestamp file
    # until match or not found
    sorted_fnames = sorted(outjsonfnames, reverse=True)
    outputjsonfile = sorted_fnames[0]
    # Use rsplit to get the timestamppart
    (filenamepart, timestamppart) = outputjsonfile.rsplit('.', 1)
    #print "Last file timestamped is (%s)" % outputjsonfile
    #print "processMatchOneLast Output json %s" % outputjsonfile
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
            # Update subgoalsresult[timestamppart][goalid] also
            subgoalsresult[timestamppart][goalid] = True
            return
    else:
        current_onlyanswer = jsonoutput[answertagstring]

        #print "Correct onlyanswer is (%s)" % current_onlyanswer

        found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
        if found:
            #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
            grades[goalid] = True
            # Update subgoalsresult[timestamppart][goalid] also
            subgoalsresult[timestamppart][goalid] = True
            return
 
    # All file processed - still not found
    if not found:
        #print "processMatchOneLast failed"
        grades[goalid] = False
        # Update subgoalsresult[timestamppart][goalid] also
        subgoalsresult[timestamppart][goalid] = False

def processBooleanSet(outjsonfnames, grades, subgoalsresult, eachgoal):
    #print "Inside processBooleanSet"
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
        # No more answer.config (parameter or parameter_ascii will become answer=<value> already)
        (use_target, answertagstring) = jsonanswertag.split('.')
        #print use_target
        #print answertagstring

    # for processBooleanSet - Process all files regardless of match found or not found
    for outputjsonfile in outjsonfnames:
        #print "processBooleanSet Output json %s" % outputjsonfile
        # Use rsplit to get the timestamppart
        (filenamepart, timestamppart) = outputjsonfile.rsplit('.', 1)
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
            # Update subgoalsresult[timestamppart][goalid] accordingly
            if found:
                #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
                subgoalsresult[timestamppart][goalid] = True
            else:
                subgoalsresult[timestamppart][goalid] = False
        else:
            answertagresult = jsonoutput[answertagstring]
            current_answer = answertagresult.strip()
            #print "Correct answer is (%s)" % current_answer
            found = compare_result_answer(resulttagresult, current_answer, eachgoal['goaloperator'])
            # Update subgoalsresult[timestamppart][goalid] accordingly
            if found:
                #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_answer)
                subgoalsresult[timestamppart][goalid] = True
            else:
                subgoalsresult[timestamppart][goalid] = False
 
    # All file processed
    print subgoalsresult

# Process Lab Exercise
def processLabExercise(studentdir, labidname, grades, subgoalsresult, goals):
    #print "Goals JSON config is"
    #print goals
    #for eachgoal in goals:
    #    print "Current goal is "
    #    print eachgoal
    #    print "    goalid is (%s)" % eachgoal['goalid']
    #    print "    goaltype is (%s)" % eachgoal['goaltype']
    #    print "    answertag is (%s)" % eachgoal['answertag']
    #    print "    resulttag is (%s)" % eachgoal['resulttag']
    #    print ""

    RESULTHOME = '%s/%s' % (studentdir, ".local/result/")
    outjsonfnames = glob.glob('%s/%s.*' % (RESULTHOME, labidname))
    #print outjsonfnames

    # Go through each goal for each student
    # Do the goaltype of non 'boolean' first
    for eachgoal in goals:
        if eachgoal['goaltype'] == "matchanyany":
            processMatchAnyAny(outjsonfnames, grades, eachgoal)
        elif eachgoal['goaltype'] == "matchoneany":
            processMatchOneAny(outjsonfnames, grades, eachgoal)
        elif eachgoal['goaltype'] == "matchonelast":
            processMatchOneLast(outjsonfnames, grades, subgoalsresult, eachgoal)
        elif eachgoal['goaltype'] == "boolean_set":
            processBooleanSet(outjsonfnames, grades, subgoalsresult, eachgoal)
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
            eachgoal['goaltype'] == "matchonelast" or
            eachgoal['goaltype'] == "boolean_set"):
            continue
        elif eachgoal['goaltype'] == "boolean":
            t_string = eachgoal['boolean_string']
            # Use subgoalsresult for processing 
            # - if found on any timestamp then True
            # - if not found on any timestamp then False
            subgoaltimestamp_found = False
            # Process all subgoalsresult[timestamppart] dictionary
            for timestamp, subgoal in subgoalsresult.iteritems():
                subgoaltimestamp_found = evalBoolean.evaluate_boolean_expression(t_string, subgoal)
                if subgoaltimestamp_found:
                    # found - break from loop
                    break
            goalid = eachgoal['goalid']
            grades[goalid] = subgoaltimestamp_found
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
    subgoalsresult = collections.defaultdict(dict)
    goalsjsonfname = '%s/.local/instr_config/%s' % (UBUNTUHOME, "goals.json")
    goalsjson = open(goalsjsonfname, "r")
    goals = json.load(goalsjson)
    goalsjson.close()
    #print "Goals JSON config is"
    #print goals

    processLabExercise(studentdir, labidname, grades, subgoalsresult, goals)
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

