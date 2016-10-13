#!/usr/bin/env python

# GoalsParser.py
# Description: * Read goals.config
#              * Create a json file

import json
import glob
import os
import sys

UBUNTUHOME = "/home/ubuntu/"
exec_proglist = []
stdinfnameslist = []
stdoutfnameslist = []
timestamplist = []
nametags = {}

class MyGoal(object):
    """ Goal - goalid, goaltype, goaloperator, tag1, tag2 """
    goalid = ""
    goaltype = ""
    goaloperator = ""
    tag1 = ""
    tag2 = ""

    def goal_dict(object):
        return object.__dict__

    def __init__(self, goalid, goaltype, goaloperator, tag1, tag2):
        self.goalid = goalid
        self.goaltype = goaltype
        self.goaloperator = goaloperator
        self.tag1 = tag1
        self.tag2 = tag2

def ValidateTag(inputtag, allowed_special_answer):
    # if allowed_special_answer is true, then allow 'answer=<string>' or 'answer.<tag>'
    returntag = ""
    if '.' in inputtag:
        #print "tag %s contains '.'" % inputtag
        (target, finaltag) = inputtag.split('.')
        if not (target == "answer" or target == "result"):
            sys.stderr.write("ERROR: goals.config contains unrecognized tag (%s)\n" % inputtag)
            sys.exit(1)
        if not finaltag.isalnum():
            sys.stderr.write("ERROR: goals.config contains tag (%s) not alphanumeric\n" % inputtag)
            sys.exit(1)
        if not allowed_special_answer:
            if target == "answer":
                sys.stderr.write("ERROR: goals.config tag2 (%s) is not allowed 'answer.<string>'\n" % inputtag)
                sys.exit(1)
        returntag = inputtag
    elif '=' in inputtag:
        if not allowed_special_answer:
            sys.stderr.write("ERROR: goals.config only tag1 is allowed answer=<string>, tag2 (%s) is not\n" % inputtag)
            sys.exit(1)
        #print "tag %s contains '='" % inputtag
        (target, finaltag) = inputtag.split('=')
        if target != "answer":
            sys.stderr.write("ERROR: goals.config tag=<string> then tag must be answer (%s)\n" % inputtag)
            sys.exit(1)
        if not finaltag.isalnum():
            sys.stderr.write("ERROR: goals.config contains tag (%s) not alphanumeric\n" % inputtag)
            sys.exit(1)
        if not finaltag.isalnum():
            sys.stderr.write("ERROR: goals.config contains tag (%s) not alphanumeric\n" % inputtag)
            sys.exit(1)
        returntag = inputtag
    else:
        #print "tag is %s" % inputtag
        if not inputtag.isalnum():
            sys.stderr.write("ERROR: goals.config contains tag (%s) not alphanumeric\n" % inputtag)
            sys.exit(1)
        returntag = 'result.%s' % inputtag

    return returntag

def ParseGoals():
    configfilename = '%s/.local/config/%s' % (UBUNTUHOME, "goals.config")
    configfile = open(configfilename)
    configfilelines = configfile.readlines()
    configfile.close()
  
    for line in configfilelines:
        linestrip = line.rstrip()
        if linestrip:
            if not linestrip.startswith('#'):
                #print "Current linestrip is (%s)" % linestrip
                (each_key, each_value) = linestrip.split('=', 1)
                each_key = each_key.strip()
                #print each_key
                #print each_value
                if not each_key.isalnum():
                    sys.stderr.write("ERROR: goals.config contains key (%s) not alphanumeric\n" % each_key)
                    sys.exit(1)
                values = []
                # expecting - <type> : <operator> : <tag1> : <tag2>
                values = each_value.split(":")
                numvalues = len(values)
                if numvalues != 4:
                    sys.stderr.write("ERROR: goals.config contains unexpected value (%s) format\n" % each_value)
                    sys.exit(1)
                goal_type = values[0].strip()
                goal_operator = values[1].strip()
                tag1 = values[2].strip()
                tag2 = values[3].strip()
                # Allowed 'answer=<string>' for tag1 only
                valid_tag1 = ValidateTag(tag1, True)
                valid_tag2 = ValidateTag(tag2, False)
                if not (goal_type == "matchanyany" or
                    goal_type == "matchoneany" or
                    goal_type == "matchonelast"):
                    sys.stderr.write("ERROR: goals.config contains unrecognized type (%s)\n" % goal_type)
                    sys.exit(1)
                if not (goal_operator == "string_equal" or
                    goal_operator == "string_diff" or
                    goal_operator == "integer_equal" or
                    goal_operator == "integer_greater" or
                    goal_operator == "integer_lessthan"):
                    sys.stderr.write("ERROR: goals.config contains unrecognized operator (%s)\n" % goal_operator)
                    sys.exit(1)
                nametags[each_key] = MyGoal(each_key, goal_type, goal_operator, valid_tag1, valid_tag2)
                #nametags[each_key].toJSON()
                #nametags[each_key].goal_type = goal_type
                #nametags[each_key].goal_operator = goal_operator
                #nametags[each_key].tag1 = valid_tag1
                #nametags[each_key].tag2 = valid_tag2

        #else:
        #    print "Skipping empty linestrip is (%s)" % linestrip


    #print nametags["crash"].toJSON()
    #for (each_key, each_goal) in nametags.items():
    #    print nametags[each_key].toJSON()
    outputjsonfname = '%s/.local/config/%s' % (UBUNTUHOME, "goals.json")
    #print "Outputjsonfname is (%s)" % outputjsonfname
        
    #print nametags
    jsonoutput = open(outputjsonfname, "w")
    jsondumpsoutput = json.dumps([nametags[each_key].goal_dict() for (each_key, each_goal) in nametags.items()], indent=4)
    jsonoutput.write(jsondumpsoutput)
    jsonoutput.write('\n')
    jsonoutput.close()

# Usage: GoalsParser.py
# Arguments:
#     None
def main():
    #print "Running GoalsParser.py"
    if len(sys.argv) != 1:
        sys.stderr.write("Usage: GoalsParser.py\n")
        sys.exit(1)

    ParseGoals()
    return 0

if __name__ == '__main__':
    sys.exit(main())

