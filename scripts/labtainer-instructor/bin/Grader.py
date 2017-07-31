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

# Grader.py
# Description: Read instructorlab.json and grade the student lab work

import collections
import filecmp
import json
import glob
import os
import sys
import ast
import string
import evalBoolean

UBUNTUHOME="/home/ubuntu/"
default_timestamp = 'default-NONE'
def compare_time_during(goal1timestamp, goal2timestamp):
    goal1start, goal1end = goal1timestamp.split('-')
    goal2start, goal2end = goal2timestamp.split('-')
    #print "goal1start (%s) goal1end (%s)" % (goal1start, goal1end)
    #print "goal2start (%s) goal2end (%s)" % (goal2start, goal2end)
    if goal1start == 'default' or goal2start == 'default':
        return False
        #print "Can't compare 'default' timestamp!"
        #exit(1)
    if goal1end == 'NONE' or goal2end == 'NONE':
        return False
        #print "Can't compare 'NONE' timestamp!"
        #exit(1)
    if goal2start <= goal1start and goal1start <= goal2end:
        #print "goal2start (%s) <= goal1start (%s) <= goal2end (%s)" % (goal1start, goal2start, goal1end)
        return True
    else:
        #print "NOT - goal2start (%s) <= goal1start (%s) <= goal2end (%s)" % (goal1start, goal2start, goal1end)
        return False

def compare_time_before(goal1timestamp, goal2timestamp):
    goal1start, goal1end = goal1timestamp.split('-')
    goal2start, goal2end = goal2timestamp.split('-')
    if goal1start == 'default' or goal2start == 'default':
        print "Can't compare 'default' timestamp!"
        exit(1)
    if goal1start <= goal2start:
        #print "goal1start (%s) <= goal2start (%s)" % (goal1start, goal2start)
        return True
    else:
        return False

def evalTimeBefore(goals_tag1, goals_tag2):
    evalTimeBeforeResult = False
    for goal1timestamp, goal1value in goals_tag1.iteritems():
        #print "Goal1 timestamp is (%s) and value is (%s)" % (goal1timestamp, goal1value)
        # For each Goal1 value that is True
        if goal1value:
            for goal2timestamp, goal2value in goals_tag2.iteritems():
                #print "Goal2 timestamp is (%s) and value is (%s)" % (goal2timestamp, goal2value)
                # If there is Goal2 value that is True
                if goal2value:
                    #print "goal1ts (%s) goal2ts (%s)" % (goal1timestamp, goal2timestamp)
                    evalTimeBeforeResult = compare_time_before(goal1timestamp, goal2timestamp)
                    if evalTimeBeforeResult:
                        # if evalTimeBeforeResult is True - that means:
                        # (1) goals_tag1 is True and goals_tag2 is True
                        # (2) goal1start <= goal2start
                        break
        if evalTimeBeforeResult:
            break

    return evalTimeBeforeResult

def evalTimeDuring(goals_tag1, goals_tag2):
    evalTimeDuringResult = False
    for goal1timestamp, goal1value in goals_tag1.iteritems():
        #print "Goal1 timestamp is (%s) and value is (%s)" % (goal1timestamp, goal1value)
        # For each Goal1 value that is True
        if goal1value:
            for goal2timestamp, goal2value in goals_tag2.iteritems():
                #print "Goal2 timestamp is (%s) and value is (%s)" % (goal2timestamp, goal2value)
                # If there is Goal2 value that is True
                if goal2value:
                    #print "goal1ts (%s) goal2ts (%s)" % (goal1timestamp, goal2timestamp)
                    evalTimeDuringResult = compare_time_during(goal1timestamp, goal2timestamp)
                    if evalTimeDuringResult:
                        # if evalTimeDuringResult is True - that means:
                        # (1) goals_tag1 is True and goals_tag2 is True
                        # (2) goal2start (%s) <= goal1start (%s) <= goal2end (%s)
                        break
        if evalTimeDuringResult:
            break

    return evalTimeDuringResult

def add_goals_id_ts(goalid, goalts, goalvalue, goals_id_ts, goals_ts_id):
    #print('add_goals_id_ts goalid %s goalts %s' % (goalid, goalts))
    # Do goals_id_ts first
    if goalid not in goals_id_ts:
        goals_id_ts[goalid] = {}
        goals_id_ts[goalid][goalts] = goalvalue
    else:
        if goalts in goals_id_ts[goalid]:
            if goalts != default_timestamp:
                # Already have that goal with that goalid and that timestamp
                print("Grader.py add_goals_id_ts(1): duplicate goalid <%s> timestamp <%s>" % (goalid, goalts))
                exit(1)
            else:
                print("Grader.py add_goals_id_ts(1): duplicate goalid <%s> timestamp <%s>" % (goalid, goalts))
                return
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

def getJsonOut(outputjsonfile):
    with open(outputjsonfile, "r") as jsonfile:
        jsonoutput = json.load(jsonfile)

    for key in jsonoutput:
        old = jsonoutput[key]
        new = ast.literal_eval(old)
        if new is not None:
            new_filtered = filter(lambda x: x in string.printable, new)
        else:
            new_filtered = "NONE"
        jsonoutput[key] = new_filtered
        #print('is %s' % new)
    return jsonoutput


def compare_result_answer(current_result, current_answer, operator):
    found = False
    result_int = None
    if "integer" in operator:
        try:
            if current_result.startswith('0x'):
                result_int = int(current_result, 16)
            else:
                result_int = int(current_result, 10)
        except ValueError:
            pass
            #print('Could not get integer from result <%s>' % current_result)
        try:
            if current_answer.startswith('0x'):
                answer_int = int(current_answer, 16)
            else:
                answer_int = int(current_answer, 10)
        except ValueError:
            pass
            #print('Could not get integer from answer <%s>' % current_answer)

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
    elif operator == "is_true":
        if current_result.lower() == 'true':
            found = True
    elif operator == "is_false":
        if current_result.lower() == 'false':
            found = True
    else:
        found = False

    return found

def processMatchLast(outjsonfnames, eachgoal, goals_id_ts, goals_ts_id):
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
    jsonoutput = getJsonOut(outputjsonfile)

    #print jsonoutput
    if jsonoutput == {}:
        # empty - skip
        return

    try:
        resulttagresult = jsonoutput[resulttag]
    except:
        #print('processMatchLast: %s not found in file %s' % (resulttag, outputjsonfile))
        return
    #print resulttagresult
    try:
        timestampend = jsonoutput['PROGRAM_ENDTIME']
    except:
        print('processMatchLast: PROGRAM_ENDTIME not found in file %s' % outputjsonfile)
        exit(1)
    fulltimestamp = '%s-%s' % (timestamppart, timestampend)
    if one_answer:
        found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
        if found:
            #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
            add_goals_id_ts(goalid, fulltimestamp, True, goals_id_ts, goals_ts_id)
            return
    else:
        current_onlyanswer = jsonoutput[answertagstring]
        #print "Correct onlyanswer is (%s)" % current_onlyanswer
        found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
        if found:
            #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
            add_goals_id_ts(goalid, fulltimestamp, True, goals_id_ts, goals_ts_id)
            return
 
    # All file processed - still not found
    if not found:
        #print "processMatchLast failed"
        add_goals_id_ts(goalid, fulltimestamp, False, goals_id_ts, goals_ts_id)

def processMatchAcross(outjsonfnames, eachgoal, goals_id_ts, goals_ts_id):
    '''  TBD, this seems wrong, should only be one answer for all timestamps? '''
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
    fulltimestamp = None
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
        jsonoutput = getJsonOut(outputjsonfile)
        #print "processMatchAcross: goalid is (%s), timestamppart is (%s)" % (goalid, timestamppart)

        #print jsonoutput
        if jsonoutput == {}:
            # empty - skip
            continue

        try:
            resulttagresult = jsonoutput[resulttag]
        except:
            #print('processMatchAcross: %s not found in file %s' % (resulttag, outputjsonfile))
            continue
        #print resulttagresult
        try:
            timestampend = jsonoutput['PROGRAM_ENDTIME']
        except:
            print('processMatchAcross: PROGRAM_ENDTIME not found in file %s' % outputjsonfile)
            exit(1)
        fulltimestamp = '%s-%s' % (timestamppart, timestampend)

        for outputjsonfile2 in outjsonfnames:
            # ensure different time stamp
            if outputjsonfile == outputjsonfile2:
                continue
            #print "processMatchAcross Output 2 json %s" % outputjsonfile
            jsonfile2 = getJsonOut(outputjsonfile2)
            try:
                current_answer = jsonfile2[answertagstring]
            except KeyError:
                #print('processMatchAcross: (2) %s not found in file %s' % (answertagstring, outputjsonfile2))
                continue

            #print "Correct answer is (%s)" % current_answer

            found = compare_result_answer(resulttagresult, current_answer, eachgoal['goaloperator'])
            if found:
                #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_answer)
                add_goals_id_ts(goalid, fulltimestamp, True, goals_id_ts, goals_ts_id)
                return
 
    # All file processed - still not found
    if not found:
        #print "processMatchAcross failed"
        add_goals_id_ts(goalid, fulltimestamp, False, goals_id_ts, goals_ts_id)

def processMatchAny(outjsonfnames, eachgoal, goals_id_ts, goals_ts_id):
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
        jsonoutput = getJsonOut(outputjsonfile)

        #print "processMatchAny: goalid is (%s), timestamppart is (%s)" % (goalid, timestamppart)
        #print jsonoutput
        if jsonoutput == {}:
            # empty - skip
            continue

        try:
            resulttagresult = jsonoutput[resulttag]
        except KeyError:
            #print('processMatchAny: %s not found in file %s' % (resulttag, outputjsonfile))
            continue
        
        #print resulttagresult
        try:
            timestampend = jsonoutput['PROGRAM_ENDTIME']
        except KeyError:
            print('processMatchAny: PROGRAM_ENDTIME not found in file %s' % outputjsonfile)
            exit(1)
        fulltimestamp = '%s-%s' % (timestamppart, timestampend)
        if one_answer:
            #print "Correct answer is (%s) result (%s)" % (current_onlyanswer, resulttagresult)
            found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
            add_goals_id_ts(goalid, fulltimestamp, found, goals_id_ts, goals_ts_id)
        else:
            answertagresult = jsonoutput[answertagstring]
            current_answer = answertagresult.strip()
            #print "Correct answer is (%s) result (%s)" % (current_answer, resulttagresult)
            found = compare_result_answer(resulttagresult, current_answer, eachgoal['goaloperator'])
            add_goals_id_ts(goalid, fulltimestamp, found, goals_id_ts, goals_ts_id)
 
    # All file processed
    #print goals_id_ts
    #print goals_ts_id

def processTrueFalse(outjsonfnames, eachgoal, goals_id_ts, goals_ts_id):
    #print "Inside processTrueFalse"
    found = False
    goalid = eachgoal['goalid']
    #print goalid
    resulttag = eachgoal['resulttag']
    #print resulttag
    #print eachgoal

    for outputjsonfile in outjsonfnames:
        #print "processTrueFalse: outputjsonfile is (%s)" % outputjsonfile
        # Use rsplit to get the timestamppart
        if outputjsonfile.endswith("student"):
            filenamepart = outputjsonfile
            timestamppart = "default"
        else:
            (filenamepart, timestamppart) = outputjsonfile.rsplit('.', 1)
        jsonoutput = getJsonOut(outputjsonfile)

        if jsonoutput == {}:
            # empty - skip
            continue

        try:
            resulttagresult = jsonoutput[resulttag]
        except KeyError:
            #print('processTrueFalse: %s not found in file %s' % (resulttag, outputjsonfile))
            continue
        
        try:
            timestampend = jsonoutput['PROGRAM_ENDTIME']
        except KeyError:
            print('processTrueFalse: PROGRAM_ENDTIME not found in file %s' % outputjsonfile)
            exit(1)
        fulltimestamp = '%s-%s' % (timestamppart, timestampend)
        #print('compare %s operator %s' % (resulttagresult, eachgoal['goaltype']))
        found = compare_result_answer(resulttagresult, None, eachgoal['goaltype'])
        add_goals_id_ts(goalid, fulltimestamp, found, goals_id_ts, goals_ts_id)
 
def countTrue(goal_list, current_goals):
    the_list = goal_list[goal_list.find("(")+1:goal_list.find(")")]
    the_goals = the_list.strip().split(',')
    the_goals = [x.strip() for x in the_goals]
    count = 0
    for item in current_goals:
        item = item.strip()
        if item in the_goals:
            if current_goals[item]:
                count += 1
    return count
    
def processCountGreater(eachgoal, goals_id_ts, goals_ts_id):
    goalid = eachgoal['goalid']
    try:
        value = int(eachgoal['answertag'])
    except:
        print('ERROR: Grader.py could not parse int from %s in %s' % (eachgoal['answertag'], eachgoal))
        exit(1)
    ''' note, not a boolean string, TBD change name to more generic '''
    subgoal_list = eachgoal['boolean_string']
    # Process all goals_ts_id dictionary
    goalid = eachgoal['goalid']
    #print('countGreater, value %d list %s' % (value, subgoal_list))
    true_count = 0
    for timestamppart, current_goals in goals_ts_id.iteritems():
        true_count += countTrue(subgoal_list, current_goals)
    is_greater = False
    if true_count > value:
        is_greater = True
    #print('countGreater result is %r' % is_greater)
    add_goals_id_ts(goalid, default_timestamp, is_greater, goals_id_ts, goals_ts_id)
    

def processTemporal(eachgoal, goals_id_ts, goals_ts_id):
    print('processTemporal')
    goal1tag = eachgoal['goal1tag']
    goal2tag = eachgoal['goal2tag']
    goalid = eachgoal['goalid']
    #print "goal1tag is (%s) and goal2tag is (%s)" % (goal1tag, goal2tag)
    # Make sure goal1tag and goal2tag is in goals_id_ts
    if goal1tag not in goals_id_ts:
        sys.stdout.write("warning: goal1tag (%s) does not exist in %s\n" % (goal1tag, eachgoal))
        return
    if goal2tag not in goals_id_ts:
        sys.stdout.write("warning: goal2tag (%s) does not exist!\n" % goal2tag)
        return
    goals_tag1 = {}
    goals_tag2 = {}
    goals_tag1 = goals_id_ts[goal1tag]
    goals_tag2 = goals_id_ts[goal2tag]
    #print "Goals tag1 is "
    #print goals_tag1
    #print "Goals tag2 is "
    #print goals_tag2
    if eachgoal['goaltype'] == "time_before":
        evalTimeResult = evalTimeBefore(goals_tag1, goals_tag2)
        # if evalTimeResult is False - that means, can't find the following condition:
        # (1) goals_tag1 is True and goals_tag2 is True
        # (2) goal1start <= goal2start
    if eachgoal['goaltype'] == "time_during":
        evalTimeResult = evalTimeDuring(goals_tag1, goals_tag2)
        # if evalTimeResult is False - that means, can't find the following condition:
        # (1) goals_tag1 is True and goals_tag2 is True
        # (2) goal2start (%s) <= goal1start (%s) <= goal2end (%s)

    #print('processTemporal %s' % goalid)
    add_goals_id_ts(goalid, default_timestamp, evalTimeResult, goals_id_ts, goals_ts_id)

def processBoolean(eachgoal, goals_id_ts, goals_ts_id):
    t_string = eachgoal['boolean_string']
    evalBooleanResult = None
    goalid = eachgoal['goalid']
    # Process all goals_ts_id dictionary
    for timestamppart, current_goals in goals_ts_id.iteritems():
        if timestamppart != default_timestamp:
            #print('eval %s against %s tspart %s' % (t_string, str(current_goals), timestamppart))
            evalBooleanResult = evalBoolean.evaluate_boolean_expression(t_string, current_goals)
            if evalBooleanResult is not None:
                add_goals_id_ts(goalid, timestamppart, evalBooleanResult, goals_id_ts, goals_ts_id)
    # if evalBooleanResult is None - means not found
    if evalBooleanResult is None:
        #print('processBoolean is None, goalid %s goal_id_ts %s' % (goalid, goals_id_ts))
        add_goals_id_ts(goalid, default_timestamp, False, goals_id_ts, goals_ts_id)

# Process Lab Exercise
def processLabExercise(studentlabdir, labidname, grades, goals, goals_id_ts, goals_ts_id):
    #print('processLabExercise studentlabdir %s ' % (studentlabdir))
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
        #print('goal is %s type %s' % (eachgoal['goalid'], eachgoal['goaltype']))

        if eachgoal['goaltype'] == "matchany":
            processMatchAny(outjsonfnames, eachgoal, goals_id_ts, goals_ts_id)
        elif eachgoal['goaltype'] == "matchlast":
            processMatchLast(outjsonfnames, eachgoal, goals_id_ts, goals_ts_id)
        elif eachgoal['goaltype'] == "matchacross":
            processMatchAcross(outjsonfnames, eachgoal, goals_id_ts, goals_ts_id)
        elif eachgoal['goaltype'] == "boolean":
            processBoolean(eachgoal, goals_id_ts, goals_ts_id)
        elif eachgoal['goaltype'] == "time_before" or \
             eachgoal['goaltype'] == "time_during":
            processTemporal(eachgoal, goals_id_ts, goals_ts_id)
        elif eachgoal['goaltype'] == "count_greater":
            processCountGreater(eachgoal, goals_id_ts, goals_ts_id)
        elif eachgoal['goaltype'].startswith('is_'):
            processTrueFalse(outjsonfnames, eachgoal, goals_id_ts, goals_ts_id)
        else:
            sys.stdout.write("Error: Invalid goal type!\n")
            sys.exit(1)


    #print "Goals - id timestamp : "
    #print goals_id_ts
    #for current_goals, timestamp in goals_id_ts.iteritems():
    #     print "-----"
    #     print current_goals
    #     print timestamp
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
        #print('assign grades[%s] %r' % (goalid, current_goals_result))
        grades[goalid] = current_goals_result

    #print grades

    return 0

# Usage: ProcessStudentLab <studentlabdir> <labidname>
# Arguments:
#     <studentlabdir> - directory containing the student lab work
#                    extracted from zip file (done in instructor.py)
#     <labidname> - labidname should represent filename of output json file
def ProcessStudentLab(studentlabdir, labidname):
    # Goals
    goals_id_ts = {}
    goals_ts_id = {}
    grades = {}
    resultsdir = os.path.join(studentlabdir, '.local','result')
    try:
        os.makedirs(resultsdir)
    except:
        pass
    goalsjsonfname = os.path.join(resultsdir,'goals.json')
    goalsjson = open(goalsjsonfname, "r")
    goals = json.load(goalsjson)
    goalsjson.close()
    #print "Goals JSON config is"
    #print goals

    processLabExercise(studentlabdir, labidname, grades, goals, goals_id_ts, goals_ts_id)
    return grades

# Usage: Grader.py <studentlabdir> <labidname>
# Arguments:
#     <studentlabdir> - directory containing the student lab work
#                    extracted from zip file (done in instructor.py)
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

