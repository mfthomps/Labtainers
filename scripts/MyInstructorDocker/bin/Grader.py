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
matchacrosslist = []

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

def processMatchAny(outjsonfnames, grades, eachgoal):
    #print "Inside processMatchAny"
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

    #print outjsonfnames
    # MatchAny - Process each file until match or not found
    for outputjsonfile in outjsonfnames:
        #print "processMatchAny Output json %s" % outputjsonfile
        jsonfile = open(outputjsonfile, "r")
        jsonoutput = json.load(jsonfile)
        jsonfile.close()

        #print jsonoutput
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
            current_onlyanswer = jsonoutput[answertagstring]

            #print "Correct onlyanswer is (%s)" % current_onlyanswer

            found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
            if found:
                #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
                grades[goalid] = True
                return
 
    # All file processed - still not found
    if not found:
        #print "processMatchAny failed"
        grades[goalid] = False

def processMatchLast(outjsonfnames, grades, subgoalsresult, eachgoal):
    #print "Inside processMatchLast"
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

    # MatchLast - Process only the last timestamp file
    # until match or not found
    sorted_fnames = sorted(outjsonfnames, reverse=True)
    outputjsonfile = sorted_fnames[0]
    # Use rsplit to get the timestamppart
    (filenamepart, timestamppart) = outputjsonfile.rsplit('.', 1)
    #print "Last file timestamped is (%s)" % outputjsonfile
    #print "processMatchLast Output json %s" % outputjsonfile
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
        #print "processMatchLast failed"
        grades[goalid] = False
        # Update subgoalsresult[timestamppart][goalid] also
        subgoalsresult[timestamppart][goalid] = False

def processMatchAcross(outjsonfnames, grades, eachgoal):
    #print "Inside processMatchAcross"
    found = False
    goalid = eachgoal['goalid']
    #print goalid
    jsonanswertag = eachgoal['answertag']
    #print jsonanswertag
    jsonresulttag = eachgoal['resulttag']
    (resulttagtarget, resulttag) = jsonresulttag.split('.')
    #print jsonresulttag
    # answer=<string> and goal_type=matchacross have been checked (not allowed)
    # during parsing of goals
    (use_target, answertagstring) = jsonanswertag.split('.')
    #print use_target
    #print answertagstring

    # MatchAcross - Process each file against other files with different timestamp
    # until match or not found
    for outputjsonfile in outjsonfnames:
        #print "processMatchAcross Output json %s" % outputjsonfile
        jsonfile = open(outputjsonfile, "r")
        jsonoutput = json.load(jsonfile)
        jsonfile.close()

        try:
            resulttagresult = jsonoutput[resulttag]
        except:
            print('%s not found in file %s' % (resulttag, outputjsonfile))
            exit(1)
        #print resulttagresult

        for outputjsonfile2 in outjsonfnames:
            # ensure different time stamp
            if outputjsonfile == outputjsonfile2:
                continue
            #print "processMatchAcross Output 2 json %s" % outputjsonfile
            jsonfile2 = open(outputjsonfile2, "r")
            jsonoutput2 = json.load(jsonfile2)
            jsonfile2.close()

            try:
                current_answer = jsonoutput2[answertagstring]
            except:
                print('%s not found in file %s' % (answertagstring, outputjsonfile2))
                exit(1)

            #print "Correct answer is (%s)" % current_answer

            found = compare_result_answer(resulttagresult, current_answer, eachgoal['goaloperator'])
            if found:
                #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_answer)
                grades[goalid] = True
                return
 
    # All file processed - still not found
    if not found:
        #print "processMatchAcross failed"
        grades[goalid] = False

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
    #print subgoalsresult

# Process Lab Exercise
def processLabExercise(studentlabdir, labidname, grades, subgoalsresult, goals):
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

    RESULTHOME = '%s/%s' % (studentlabdir, ".local/result/")
    #print RESULTHOME
    if not os.path.exists(RESULTHOME):
        os.makedirs(RESULTHOME)
    # Note: outputjson now may include no timestamp
    outjsonfnamesstring = '%s/*/%s/%s*' % (studentlabdir, ".local/result/", labidname)
    #print outjsonfnamesstring
    #outjsonfnames = glob.glob('%s/*/%s*' % (RESULTHOME, labidname))
    outjsonfnames = glob.glob(outjsonfnamesstring)
    #print outjsonfnames

    # Go through each goal for each student
    # Do the goaltype of non 'boolean' first
    for eachgoal in goals:
        if eachgoal['goaltype'] == "matchany":
            # DO NOT pass subgoalsresult to processMatchAny
            # goal_type matchany can't be subgoals
            processMatchAny(outjsonfnames, grades, eachgoal)
        elif eachgoal['goaltype'] == "matchlast":
            processMatchLast(outjsonfnames, grades, subgoalsresult, eachgoal)
        elif eachgoal['goaltype'] == "matchacross":
            # DO NOT pass subgoalsresult to processMatchAcross
            # goal_type matchacross can't be subgoals
            processMatchAcross(outjsonfnames, grades, eachgoal)
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
        if (eachgoal['goaltype'] == "matchany" or
            eachgoal['goaltype'] == "matchlast" or
            eachgoal['goaltype'] == "matchacross" or
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

# Usage: ProcessStudentLab <studentlabdir> <instructordir> <labidname>
# Arguments:
#     <studentlabdir> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
#     <instructordir> - directory containing instructor's solution
#                       for corresponding student
#     <labidname> - labidname should represent filename of output json file
def ProcessStudentLab(studentlabdir, instructordir, labidname):
    grades = {}
    subgoalsresult = collections.defaultdict(dict)
    goalsjsonfname = '%s/.local/instr_config/%s' % (UBUNTUHOME, "goals.json")
    goalsjson = open(goalsjsonfname, "r")
    goals = json.load(goalsjson)
    goalsjson.close()
    #print "Goals JSON config is"
    #print goals

    processLabExercise(studentlabdir, labidname, grades, subgoalsresult, goals)
    return grades

# Usage: Grader.py <studentlabdir> <instructordir> <labidname>
# Arguments:
#     <studentlabdir> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
#     <instructordir> - directory containing instructor's solution
#                       for corresponding student
#     <labidname> - labidname should represent filename of output json file
def main():
    #print "Running Grader.py"
    if len(sys.argv) != 4:
        sys.stderr.write("Usage: Grader.py <studentlabdir> <instructordir> <labidname>\n")
        return 1

    studentlabdir = sys.argv[1]
    instructordir = sys.argv[2]
    labidname = sys.argv[3]
    #print "Inside main, about to call ProcessStudentLab "

    ProcessStudentLab(studentlabdir, instructordir, labidname)

if __name__ == '__main__':
    sys.exit(main())

