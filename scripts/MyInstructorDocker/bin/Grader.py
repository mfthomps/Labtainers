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

# Goals
goals_id_ts = {}
goals_ts_id = {}

def add_goals_id_ts(goalid, goalts, goalvalue):
    # Do goals_id_ts first
    if goalid not in goals_id_ts:
        goals_id_ts[goalid] = {}
        goals_id_ts[goalid][goalts] = goalvalue
    else:
        if goalts in goals_id_ts[goalid]:
            # Already have that goal with that goalid and that timestamp
            print("Grader.py add_goals_id_ts(1): duplicate goalid timestamp!")
            exit(1)
        else:
            goals_id_ts[goalid][goalts] = goalvalue
    # Do goals_ts_id next
    if goalts not in goals_ts_id:
        goals_ts_id[goalts] = {}
        goals_ts_id[goalts][goalid] = goalvalue
    else:
        if goalid in goals_ts_id[goalts]:
            # Already have that goal with that goalid and that timestamp
            print("Grader.py add_goals_id_ts(2): duplicate goalid timestamp!")
            exit(1)
        else:
            goals_ts_id[goalts][goalid] = goalvalue


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

def processMatchLast(outjsonfnames, eachgoal):
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
    #print "processMatchLast: outputjsonfile is (%s)" % outputjsonfile
    if outputjsonfile.endswith("student"):
        filenamepart = outputjsonfile
        timestamppart = "default"
    else:
        (filenamepart, timestamppart) = outputjsonfile.rsplit('.', 1)
    #print "processMatchLast: Last file timestamped is (%s)" % outputjsonfile
    #print "processMatchLast: Output json %s" % outputjsonfile
    jsonfile = open(outputjsonfile, "r")
    jsonoutput = json.load(jsonfile)
    jsonfile.close()
    #print "processMatchLast: goalid is (%s), timestamppart is (%s)" % (goalid, timestamppart)

    #print jsonoutput
    if jsonoutput == {}:
        # empty - skip
        return

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
            add_goals_id_ts(goalid, timestamppart, True)
            return
    else:
        current_onlyanswer = jsonoutput[answertagstring]
        #print "Correct onlyanswer is (%s)" % current_onlyanswer
        found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
        if found:
            #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
            add_goals_id_ts(goalid, timestamppart, True)
            return
 
    # All file processed - still not found
    if not found:
        #print "processMatchLast failed"
        add_goals_id_ts(goalid, timestamppart, False)

def processMatchAcross(outjsonfnames, eachgoal):
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
        #print "processMatchAcross: outputjsonfile is (%s)" % outputjsonfile
        #print "processMatchAcross Output json %s" % outputjsonfile
        # Use rsplit to get the timestamppart
        if outputjsonfile.endswith("student"):
            filenamepart = outputjsonfile
            timestamppart = "default"
        else:
            (filenamepart, timestamppart) = outputjsonfile.rsplit('.', 1)
        jsonfile = open(outputjsonfile, "r")
        jsonoutput = json.load(jsonfile)
        jsonfile.close()
        #print "processMatchAcross: goalid is (%s), timestamppart is (%s)" % (goalid, timestamppart)

        #print jsonoutput
        if jsonoutput == {}:
            # empty - skip
            continue

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
                add_goals_id_ts(goalid, timestamppart, True)
                return
 
    # All file processed - still not found
    if not found:
        #print "processMatchAcross failed"
        add_goals_id_ts(goalid, timestamppart, False)

def processMatchAny(outjsonfnames, eachgoal):
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

    # for processMatchAny - Process all files regardless of match found or not found
    for outputjsonfile in outjsonfnames:
        #print "processMatchAny: outputjsonfile is (%s)" % outputjsonfile
        #print "processMatchAny Output json %s" % outputjsonfile
        # Use rsplit to get the timestamppart
        if outputjsonfile.endswith("student"):
            filenamepart = outputjsonfile
            timestamppart = "default"
        else:
            (filenamepart, timestamppart) = outputjsonfile.rsplit('.', 1)
        jsonfile = open(outputjsonfile, "r")
        jsonoutput = json.load(jsonfile)
        jsonfile.close()

        #print "processMatchAny: goalid is (%s), timestamppart is (%s)" % (goalid, timestamppart)
        #print jsonoutput
        if jsonoutput == {}:
            # empty - skip
            continue

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
                add_goals_id_ts(goalid, timestamppart, True)
            else:
                add_goals_id_ts(goalid, timestamppart, False)
        else:
            answertagresult = jsonoutput[answertagstring]
            current_answer = answertagresult.strip()
            #print "Correct answer is (%s)" % current_answer
            found = compare_result_answer(resulttagresult, current_answer, eachgoal['goaloperator'])
            if found:
                #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_answer)
                add_goals_id_ts(goalid, timestamppart, True)
            else:
                add_goals_id_ts(goalid, timestamppart, False)
 
    # All file processed
    #print goals_id_ts
    #print goals_ts_id

# Process Lab Exercise
def processLabExercise(studentlabdir, labidname, grades, goals):
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
        sys.stderr.write("ERROR: missing RESULTHOME (%s)\n" % RESULTHOME)
        sys.exit(1)
    # Note: outputjson now may include no timestamp
    #print outjsonfnames
    outjsonfnamesstring = '%s/%s/%s*' % (studentlabdir, ".local/result/", labidname)
    #print "processLabExercise: outjsonfnamestring is (%s)" % outjsonfnamesstring
    outjsonfnames = glob.glob(outjsonfnamesstring)
    #print "outputjsonfnames is "
    #print outjsonfnames

    # Go through each goal for each student
    # Do the goaltype of non 'boolean' first
    for eachgoal in goals:
        if eachgoal['goaltype'] == "matchany":
            processMatchAny(outjsonfnames, eachgoal)
        elif eachgoal['goaltype'] == "matchlast":
            processMatchLast(outjsonfnames, eachgoal)
        elif eachgoal['goaltype'] == "matchacross":
            processMatchAcross(outjsonfnames, eachgoal)
        elif eachgoal['goaltype'] == "boolean":
            #print "Skipping %s" % eachgoal
            continue
        else:
            sys.stdout.write("Error: Invalid goal type!\n")
            sys.exit(1)

    #for current_goals, timestamp in goals_id_ts.iteritems():
    #    print "current_goals is "
    #    print current_goals
    #    for key, value in timestamp.iteritems():
    #        print "Key is (%s) - value is (%s)" % (key, value)

    # Now do the goaltype of 'boolean'
    for eachgoal in goals:
        if (eachgoal['goaltype'] == "matchany" or
            eachgoal['goaltype'] == "matchlast" or
            eachgoal['goaltype'] == "matchacross"):
            continue
        elif eachgoal['goaltype'] == "boolean":
            t_string = eachgoal['boolean_string']
            evalBooleanResult = False
            # Process all goals_ts_id dictionary
            for timestamppart, current_goals in goals_ts_id.iteritems():
                evalBooleanResult = evalBoolean.evaluate_boolean_expression(t_string, current_goals)
                if evalBooleanResult:
                    # found - break from loop
                    goalid = eachgoal['goalid']
                    add_goals_id_ts(goalid, timestamppart, evalBooleanResult)
                    break
            # if evalBooleanResult is False - means not found
            if evalBooleanResult == False:
                add_goals_id_ts(goalid, "default", False)
        else:
            sys.stdout.write("Error: Invalid goal type!\n")

    #print "Goals - id timestamp : "
    #print goals_id_ts
    #print "Goals - timestamp id : "
    #print goals_ts_id

    # Now generate the grades - based on goalid
    for eachgoal in goals:
        goalid = eachgoal['goalid']
        #print "goalid is (%s)" % goalid
        # Skip goalid that starts with "_"
        if goalid.startswith('_'):
            continue
        current_goals_result = False
        for current_goals, timestamp in goals_id_ts.iteritems():
            #print "current_goals is "
            #print current_goals
            if current_goals == goalid:
                current_value = False
                # Use goals_ts_id for processing 
                # - if found on any timestamp then True
                # - if not found on any timestamp then False
                for key, value in timestamp.iteritems():
                    #print "Key is (%s) - value is (%s)" % (key, value)
                    if value:
                        current_value = True
                        break
                current_goals_result = current_value
                break
        grades[goalid] = current_goals_result

    #print grades

    return 0

# Usage: ProcessStudentLab <studentlabdir> <labidname>
# Arguments:
#     <studentlabdir> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
#     <labidname> - labidname should represent filename of output json file
def ProcessStudentLab(studentlabdir, labidname):
    grades = {}
    goalsjsonfname = '%s/.local/instr_config/%s' % (UBUNTUHOME, "goals.json")
    goalsjson = open(goalsjsonfname, "r")
    goals = json.load(goalsjson)
    goalsjson.close()
    #print "Goals JSON config is"
    #print goals

    processLabExercise(studentlabdir, labidname, grades, goals)
    return grades

# Usage: Grader.py <studentlabdir> <labidname>
# Arguments:
#     <studentlabdir> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
#     <labidname> - labidname should represent filename of output json file
def main():
    #print "Running Grader.py"
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: Grader.py <studentlabdir> <labidname>\n")
        return 1

    studentlabdir = sys.argv[1]
    labidname = sys.argv[2]
    #print "Inside main, about to call ProcessStudentLab "

    ProcessStudentLab(studentlabdir, labidname)

if __name__ == '__main__':
    sys.exit(main())

