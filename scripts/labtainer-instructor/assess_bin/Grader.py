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
# Description: Grade the student lab work

import collections
import filecmp
import json
import glob
import os
import sys
import subprocess
import ast
import string
import evalBoolean
import evalExpress
import InstructorLogging


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
                    print "goal1ts (%s) goal2ts (%s)" % (goal1timestamp, goal2timestamp)
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
                print("Grader.py add_goals_id_ts(1): duplicate goalid <%s> timestamp <%s> exit" % (goalid, goalts))
                exit(1)
            else:
                print("Grader.py add_goals_id_ts(1): duplicate goalid <%s> timestamp <%s>, return" % (goalid, goalts))
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

def getJsonOutTS(outputjsonfile):
    jsonoutput = None
    with open(outputjsonfile, "r") as jsonfile:
        jsonoutput = json.load(jsonfile)
    if jsonoutput is None:
        return None
    for ts in jsonoutput:
        result_set = jsonoutput[ts]
        for key in result_set:
            old = result_set[key]
            new = ast.literal_eval(old)
            if new is not None:
                if type(new) is str:
                    new_filtered = filter(lambda x: x in string.printable, new)
                else:
                    new_filtered = new
            else:
                new_filtered = "NONE"
            result_set[key] = new_filtered 
        jsonoutput[ts] = result_set
        #print('is %s' % new)
    return jsonoutput

def getJsonOut(outputjsonfile):
    with open(outputjsonfile, "r") as jsonfile:
        jsonoutput = json.load(jsonfile)

    for key in jsonoutput:
        old = jsonoutput[key]
        new = ast.literal_eval(old)
        if new is not None:
            if type(new) is str:
                new_filtered = filter(lambda x: x in string.printable, new)
            else:
                new_filtered = new
        else:
            new_filtered = "NONE"
        jsonoutput[key] = new_filtered
        #print('is %s' % new)
    return jsonoutput


def compare_result_answer(current_result, current_answer, operator):
    found = False
    result_int = None
    # current_result may be an int, so turn to string first so
    # we can change it back!
    current_result = str(current_result)
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

def processMatchLast(result_sets, eachgoal, goals_id_ts, goals_ts_id):
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
    results, ts = result_sets.getLatest()
    #print results
    if results == {}:
        # empty - skip
        return

    try:
        resulttagresult = results[resulttag]
    except:
        #print('processMatchLast: %s not found in file %s' % (resulttag, outputjsonfile))
        return
    #print resulttagresult
    try:
        timestampend = results['PROGRAM_ENDTIME']
    except:
        print('processMatchLast: PROGRAM_ENDTIME not found in file %s' % outputjsonfile)
        exit(1)
    fulltimestamp = '%s-%s' % (ts, timestampend)
    if one_answer:
        found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
        if found:
            #print "resulttagresult is (%s) matches answer (%s)" % (resulttagresult, current_onlyanswer)
            add_goals_id_ts(goalid, fulltimestamp, True, goals_id_ts, goals_ts_id)
            return
    else:
        current_onlyanswer = results[answertagstring]
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

def processMatchAcross(result_sets, eachgoal, goals_id_ts, goals_ts_id):
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
    for ts in result_sets.getStamps():
        results = result_sets.getSet(ts)

        #print results
        if results == {}:
            # empty - skip
            continue

        try:
            resulttagresult = results[resulttag]
        except:
            #print('processMatchAcross: %s not found in file %s' % (resulttag, outputjsonfile))
            continue
        #print resulttagresult
        try:
            timestampend = results['PROGRAM_ENDTIME']
        except:
            print('processMatchAcross: PROGRAM_ENDTIME not found in file %s' % outputjsonfile)
            exit(1)
        fulltimestamp = '%s-%s' % (ts, timestampend)

        for ts2 in result_sets.getStamps():
            # ensure different time stamp
            if ts == ts2:
                continue
            #print "processMatchAcross Output 2 json %s" % outputjsonfile
            results2 = result_sets.getSet(ts2)
            try:
                current_answer = results2[answertagstring]
            except KeyError:
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

def handle_expression(resulttag, json_output, logger):
    result = 'NONE'
    if resulttag.startswith('(') and resulttag.endswith(')'):
        express = resulttag[resulttag.find("(")+1:resulttag.find(")")]
        for tag in json_output:
            logger.DEBUG('is tag %s in express %s' % (tag, express))
            if tag in express:
                if json_output[tag] != 'NONE':
                    express = express.replace(tag, json_output[tag])
                else:
                    return 'NONE'
        try:
            logger.DEBUG('try eval of <%s>' % express)
            result = evalExpress.eval_expr(express)
        except:
            logger.ERROR('could not evaluation %s, which became %s' % (resulttag, express))
            sys.exit(1)
    else:
        logger.ERROR('handleExpress called with %s, expected expression in parens' % resulttag)
    return result

        
def processMatchAny(result_sets, eachgoal, goals_id_ts, goals_ts_id, logger):
    #print "Inside processMatchAny"
    logger.DEBUG("Inside processMatchAny")
    found = False
    goalid = eachgoal['goalid']
    #print goalid
    jsonanswertag = eachgoal['answertag']
    logger.DEBUG('jsonanswertag %s' % jsonanswertag)
    jsonresulttag = eachgoal['resulttag']
    (resulttagtarget, resulttag) = jsonresulttag.split('.')
    logger.DEBUG('jsonresulttag %s' % jsonresulttag)
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
    for ts in result_sets.getStamps():
        results = result_sets.getSet(ts)
        if results == {}:
            # empty - skip
            print('empty for ts %s' % ts)
            continue

        if resulttag.startswith('('):
            resulttagresult = str(handle_expression(resulttag, results, logger))
            logger.DEBUG('from handle_expression, got %s' % resulttagresult)
        else:
            try:
                resulttagresult = results[resulttag]
            except KeyError:
                logger.DEBUG('%s not found in file %s' % (resulttag, ts))
                continue
        
        #print resulttagresult
        try:
            timestampend = results['PROGRAM_ENDTIME']
        except KeyError:
            logger.ERROR('processMatchAny: PROGRAM_ENDTIME not found in file %s' % ts)
            exit(1)
        fulltimestamp = '%s-%s' % (ts, timestampend)
        if one_answer:
            logger.DEBUG("Correct answer is (%s) result (%s)" % (current_onlyanswer, resulttagresult))
            found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
            add_goals_id_ts(goalid, fulltimestamp, found, goals_id_ts, goals_ts_id)
        else:
            if answertagstring not in results:
                logger.ERROR('%s not in results %s' % (answertagstring, str(results)))
                sys.exit(1)
            answertagresult = results[answertagstring]
            current_answer = answertagresult.strip()
            logger.DEBUG("Correct answer is (%s) result (%s)" % (current_answer, resulttagresult))
            found = compare_result_answer(resulttagresult, current_answer, eachgoal['goaloperator'])
            add_goals_id_ts(goalid, fulltimestamp, found, goals_id_ts, goals_ts_id)

def processValue(result_sets, eachgoal, grades, logger):
    ''' assign the grade the most recent non-NONE result '''
    goalid = eachgoal['goalid']
    #print goalid
    jsonanswertag = eachgoal['answertag']
    #print jsonanswertag
    resulttag = eachgoal['resulttag']
    if resulttag.startswith('result.'):
       resulttag = resulttag[len('result.'):]

    value = 'NONE' 
    for ts in result_sets.getStamps():
        results = result_sets.getSet(ts)

        if results == {}:
            # empty - skip
            continue

        try:
            resulttagresult = results[resulttag]
        except KeyError:
            #print('processCount: %s not found in file %s' % (resulttag, outputjsonfile))
            continue
        if resulttagresult != 'NONE':        
            value = resulttagresult
    #print 'count is %d' % count
    grades[goalid] = value
 
def processCount(result_sets, eachgoal, grades, logger):
    #print "Inside processCount"
    count = 0
    goalid = eachgoal['goalid']
    #print goalid
    jsonanswertag = eachgoal['answertag']
    #print jsonanswertag
    resulttag = eachgoal['resulttag']
    if resulttag.startswith('result.'):
       resulttag = resulttag[len('result.'):]
 
    for ts in result_sets.getStamps():
        results = result_sets.getSet(ts)

        if results == {}:
            # empty - skip
            continue

        try:
            resulttagresult = results[resulttag]
        except KeyError:
            #print('processCount: %s not found in file %s' % (resulttag, outputjsonfile))
            continue
        if resulttagresult != 'NONE':        
            if 'goaloperator' in eachgoal and len(eachgoal['goaloperator']) > 0:
                jsonanswertag = eachgoal['answertag']
                #print jsonanswertag
                jsonresulttag = eachgoal['resulttag']
                print 'tag is %s' %  jsonresulttag
                #(resulttagtarget, resulttag) = jsonresulttag.split('.')
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
                    (use_target, answertagstring) = jsonanswertag.split('.')
                    #print use_target
                    #print answertagstring
                if one_answer:
                    #print "Correct answer is (%s) result (%s)" % (current_onlyanswer, resulttagresult)
                    found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])
                else:
                    if answertagstring not in results:
                        logger.ERROR('%s not in results %s' % (answertagstring, str(results)))
                        sys.exit(1)
                    answertagresult = results[answertagstring]
                    current_answer = answertagresult.strip()
                    found = compare_result_answer(resulttagresult, current_answer, eachgoal['goaloperator'])
                if found:
                    count += 1
            else:
                count += 1
    #print 'count is %d' % count
    grades[goalid] = count

def processExecute(results, eachgoal, goals_id_ts, goals_ts_id):
    #print "Inside processExecute"
    found = False
    goalid = eachgoal['goalid']
    #print goalid
    executefile = eachgoal['goaloperator']
    #print executefile
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
        print('processExecute: expecting answertag to be the parameterized value')
        exit(1)

    # for processExecute - Process all files regardless of match found or not found
    for ts in result_sets.getStamps():
        results = result_sets.getSet(ts)
        if results == {}:
            # empty - skip
            continue

        try:
            resulttagresult = results[resulttag]
        except KeyError:
            print('processExecute: %s not found in file %s' % (resulttag, outputjsonfile))
            continue
        #print resulttagresult
        
        try:
            timestampend = results['PROGRAM_ENDTIME']
        except KeyError:
            print('processExecute: PROGRAM_ENDTIME not found in file %s' % outputjsonfile)
            exit(1)
        fulltimestamp = '%s-%s' % (ts, timestampend)

        #print "Correct answer is (%s) result (%s)" % (current_onlyanswer, resulttagresult)
        #found = compare_result_answer(resulttagresult, current_onlyanswer, eachgoal['goaloperator'])

        command = "%s %s %s" % (executefile, resulttagresult, current_onlyanswer)
        #print("Command to execute is (%s)" % command)
        result = subprocess.call(command, shell=True)
        if result:
            #print "processExecute return 1"
            add_goals_id_ts(goalid, fulltimestamp, True, goals_id_ts, goals_ts_id)
        else:
            #print "processExecute return 0"
            add_goals_id_ts(goalid, fulltimestamp, False, goals_id_ts, goals_ts_id)

def processTrueFalse(result_sets, eachgoal, goals_id_ts, goals_ts_id):
    #print "Inside processTrueFalse"
    found = False
    goalid = eachgoal['goalid']
    #print goalid
    resulttag = eachgoal['resulttag']
    #print resulttag
    #print eachgoal

    for ts in result_sets.getStamps():
        results = result_sets.getSet(ts)

        if results == {}:
            # empty - skip
            continue

        try:
            resulttagresult = results[resulttag]
        except KeyError:
            #print('processTrueFalse: %s not found in file %s' % (resulttag, outputjsonfile))
            continue
        
        try:
            timestampend = results['PROGRAM_ENDTIME']
        except KeyError:
            print('processTrueFalse: PROGRAM_ENDTIME not found in file %s' % outputjsonfile)
            exit(1)
        fulltimestamp = '%s-%s' % (ts, timestampend)
        #print('compare %s operator %s' % (resulttagresult, eachgoal['goaltype']))
        found = compare_result_answer(resulttagresult, None, eachgoal['goaltype'])
        add_goals_id_ts(goalid, fulltimestamp, found, goals_id_ts, goals_ts_id)
 
def countTrue(the_goals, current_goals):
    #print('current goals %s' % str(current_goals))
    count = 0
    for item in current_goals:
        item = item.strip()
        if item in the_goals:
            if current_goals[item]:
                count += 1
                #print('item %s true count now %d' % (item, count))
                the_goals.remove(item)
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
    the_list = subgoal_list[subgoal_list.find("(")+1:subgoal_list.find(")")]
    the_goals = the_list.strip().split(',')
    the_goals = [x.strip() for x in the_goals]
    for timestamppart, current_goals in goals_ts_id.iteritems():
        true_count += countTrue(the_goals, current_goals)
        #print('true_count now %d' % true_count)
    is_greater = False
    if true_count > value:
        is_greater = True
    #print('true_count is %d' % true_count)
    #print('countGreater result is %r' % is_greater)
    add_goals_id_ts(goalid, default_timestamp, is_greater, goals_id_ts, goals_ts_id)
    

def processTemporal(eachgoal, goals_id_ts, goals_ts_id, logger):
    goal1tag = eachgoal['goal1tag']
    goal2tag = eachgoal['goal2tag']
    goalid = eachgoal['goalid']
    logger.DEBUG("goal1tag is (%s) and goal2tag is (%s)" % (goal1tag, goal2tag))
    # Make sure goal1tag and goal2tag is in goals_id_ts
    if goal1tag not in goals_id_ts:
        logger.DEBUG("warning: goal1tag (%s) does not exist in %s\n" % (goal1tag, str(goals_id_ts)))
        return
    if goal2tag not in goals_id_ts:
        logger.DEBUG("warning: goal2tag (%s) does not exist!\n" % goal2tag)
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
        logger.DEBUG('eval for %s %s' % (goals_tag1, goals_tag2))
        evalTimeResult = evalTimeDuring(goals_tag1, goals_tag2)
        # if evalTimeResult is False - that means, can't find the following condition:
        # (1) goals_tag1 is True and goals_tag2 is True
        # (2) goal2start (%s) <= goal1start (%s) <= goal2end (%s)

    add_goals_id_ts(goalid, default_timestamp, evalTimeResult, goals_id_ts, goals_ts_id)

def processBoolean(eachgoal, goals_id_ts, goals_ts_id, logger):
    t_string = eachgoal['boolean_string']
    evalBooleanResult = None
    goalid = eachgoal['goalid']
    # Process all goals_ts_id dictionary
    for timestamppart, current_goals in goals_ts_id.iteritems():
        if timestamppart != default_timestamp:
            logger.DEBUG('eval %s against %s tspart %s' % (t_string, str(current_goals), timestamppart))
            evalBooleanResult = evalBoolean.evaluate_boolean_expression(t_string, current_goals, logger)
            if evalBooleanResult is not None:
                add_goals_id_ts(goalid, timestamppart, evalBooleanResult, goals_id_ts, goals_ts_id)
    # if evalBooleanResult is None - means not found
    if evalBooleanResult is None:
        logger.DEBUG('processBoolean is None, goalid %s goal_id_ts %s' % (goalid, goals_id_ts))
        add_goals_id_ts(goalid, default_timestamp, False, goals_id_ts, goals_ts_id)

class ResultSets():
    def addSet(self, result_set, ts):
        if ts in self.result_sets:
            for key in result_set:
                self.result_sets[ts][key] = result_set[key]
        else:
            self.result_sets[ts] = result_set

    def __init__(self, result_file_list):
        ''' result_file_list are full paths '''
        self.result_sets = {}
        self.latest = None
        for result_file in result_file_list:
            fname = os.path.basename(result_file)
            print('addSet %s' % fname)
            if '.' in fname:
                dumb, ts = fname.rsplit('.',1)
                if self.latest is None or ts > self.latest:
                    self.latest = ts
                result_set = getJsonOut(result_file)
                self.addSet(result_set, ts)
            elif fname.endswith('_ts'):
                result_set_set = getJsonOutTS(result_file)
                for ts in result_set_set:
                    self.addSet(result_set_set[ts], ts)
            else:
                result_set = getJsonOut(result_file)
                self.addSet(result_set, 'default')

    def getSet(self, ts):
        return self.result_sets[ts]
    def getLatest(self):
        return self.result_sets[self.latest], self.latest
    def getStamps(self):
        return list(self.result_sets.keys())
         


# Process Lab Exercise
def processLabExercise(studentlabdir, labidname, grades, goals, goals_id_ts, goals_ts_id, logger):
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

    ''' Read result sets '''

    outjsonfnamesstring = '%s/%s/%s*' % (studentlabdir, ".local/result/", labidname)

    outjsonfnames = glob.glob(outjsonfnamesstring)
    result_sets = ResultSets(outjsonfnames)

    # Go through each goal for each student
    # Do the goaltype of non 'boolean' first
    for eachgoal in goals:
        #print('goal is %s type %s' % (eachgoal['goalid'], eachgoal['goaltype']))

        if eachgoal['goaltype'] == "matchany":
            processMatchAny(result_sets, eachgoal, goals_id_ts, goals_ts_id, logger)
        elif eachgoal['goaltype'] == "matchlast":
            processMatchLast(result_sets, eachgoal, goals_id_ts, goals_ts_id)
        elif eachgoal['goaltype'] == "matchacross":
            processMatchAcross(result_sets, eachgoal, goals_id_ts, goals_ts_id)
        elif eachgoal['goaltype'] == "execute":
            processExecute(result_sets, eachgoal, goals_id_ts, goals_ts_id)
        elif eachgoal['goaltype'] == "boolean":
            processBoolean(eachgoal, goals_id_ts, goals_ts_id, logger)
        elif eachgoal['goaltype'] == "time_before" or \
             eachgoal['goaltype'] == "time_during":
            processTemporal(eachgoal, goals_id_ts, goals_ts_id, logger)
        elif eachgoal['goaltype'] == "count_greater":
            processCountGreater(eachgoal, goals_id_ts, goals_ts_id)
        elif eachgoal['goaltype'] == "count":
            processCount(result_sets, eachgoal, grades, logger)
        elif eachgoal['goaltype'] == "value":
            processValue(result_sets, eachgoal, grades, logger)
        elif eachgoal['goaltype'].startswith('is_'):
            processTrueFalse(result_sets, eachgoal, goals_id_ts, goals_ts_id)
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
        if goalid in grades:
            # already there, must be calculated value
            continue
        #print "goalid is (%s)" % goalid
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
#   return a dictionary of grades for this student.
# Arguments:
#     <studentlabdir> - directory containing the student lab work
#                    extracted from zip file (done in instructor.py)
#     <labidname> - labidname should represent filename of output json file
def ProcessStudentLab(studentlabdir, labidname, logger):
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

    processLabExercise(studentlabdir, labidname, grades, goals, goals_id_ts, goals_ts_id, logger)
    
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

    logger = InstructorLogging.InstructorLogging("/tmp/instructor.log")
    ProcessStudentLab(studentlabdir, labidname, logger)

if __name__ == '__main__':
    sys.exit(main())

