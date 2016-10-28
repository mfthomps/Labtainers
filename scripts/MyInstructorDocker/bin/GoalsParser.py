#!/usr/bin/env python

# GoalsParser.py
# Description: * Read goals.config
#              * Create a json file

import json
import glob
import md5
import os
import random
import sys

UBUNTUHOME = "/home/ubuntu/"
exec_proglist = []
stdinfnameslist = []
stdoutfnameslist = []
timestamplist = []
nametags = {}

class MyGoal(object):
    """ Goal - goalid, goaltype, goaloperator, answertag, resulttag """
    goalid = ""
    goaltype = ""
    goaloperator = ""
    answertag = ""
    resulttag = ""

    def goal_dict(object):
        return object.__dict__

    def __init__(self, goalid, goaltype, goaloperator, answertag, resulttag):
        self.goalid = goalid
        self.goaltype = goaltype
        self.goaloperator = goaloperator
        self.answertag = answertag
        self.resulttag = resulttag

def getRandom(bounds, type):
    # Converts lowerbound and upperbound as integer - and pass to
    # random.randint(a,b)
    # Starts with assuming will use integer (instead of hexadecimal)
    use_integer = True
    lowerboundstr = bounds[0].strip()
    if lowerboundstr.startswith('0x'):
        use_integer = False
        lowerbound_int = int(lowerboundstr, 16)
    else:
        lowerbound_int = int(lowerboundstr, 10)
    upperboundstr = bounds[1].strip()
    if upperboundstr.startswith('0x'):
        if use_integer == True:
            # Inconsistent format of lowerbound (integer format)
            # vs upperbound (hexadecimal format)
            sys.stderr.write("ERROR: inconsistent lowerbound (%s) & upperbound (%s) format\n"
                             % (lowerboundstr, upperboundstr))
            sys.exit(1)
        use_integer = False
        upperbound_int = int(upperboundstr, 16)
    else:
        upperbound_int = int(upperboundstr, 10)
    #print "lowerbound is (%d)" % lowerbound_int
    #print "upperbound is (%d)" % upperbound_int
    if lowerbound_int > upperbound_int:
        sys.stderr.write("ERROR: lowerbound greater than upperbound\n")
        sys.exit(1)
    if type == "asciirandom":
        # Make sure lowerbound/upperbound in ASCII printable characters range
        # (i.e., starts with 33-126 - excludes 33 (space) and 127 (del)
        ASCIIlowrange = 33
        ASCIIhighrange = 126
        if (lowerbound_int < ASCIIlowrange or upperbound_int > ASCIIhighrange):
            sys.stderr.write("ERROR: ASCII lowerbound (%s) & upperbound (%s) outside printable\n"
                             % (lowerboundstr, upperboundstr))
            sys.exit(1)
    random_int = random.randint(lowerbound_int, upperbound_int)
    if type == "asciirandom":
        random_str = '%s' % chr(random_int)
    elif type == "hexrandom":
        random_str = '%s' % hex(random_int)
    else:
        # type == "intrandom":
        random_str = '%s' % int(random_int)
    return random_str

def generateSpecialTagValue(studentdir, target, finaltag):
    STUDENT_LAB_INSTANCE_SEED = '%s/%s' % (studentdir, ".local/.seed")
    student_lab_instance_seedfile = open(STUDENT_LAB_INSTANCE_SEED, 'r')
    student_lab_instance_seed = student_lab_instance_seedfile.read().strip()
    student_lab_instance_seedfile.close()
    print "Student Lab instance seed is (%s)" % student_lab_instance_seed
    
    # Seed random with student lab instance seed
    random.seed(student_lab_instance_seed)

    if target == "answer":
        returnTagValue = 'answer=%s' % finaltag
    elif target == "asciirandom":
        # finaltag consists of <lowerbound>-<upperbound>
        bounds = finaltag.split('-')
        if len(bounds) != 2:
            sys.stderr.write("ERROR: asciirandom expecting <LowerBound>-<UpperBound>\n")
            sys.exit(1)
        randomstring = getRandom(bounds, "asciirandom")
        returnTagValue = 'answer=%s' % randomstring
    elif target == "hexrandom":
        # finaltag consists of <lowerbound>-<upperbound>
        bounds = finaltag.split('-')
        if len(bounds) != 2:
            sys.stderr.write("ERROR: hexrandom expecting <LowerBound>-<UpperBound>\n")
            sys.exit(1)
        randomstring = getRandom(bounds, "hexrandom")
        returnTagValue = 'answer=%s' % randomstring
    elif target == "intrandom":
        # finaltag consists of <lowerbound>-<upperbound>
        bounds = finaltag.split('-')
        if len(bounds) != 2:
            sys.stderr.write("ERROR: intrandom expecting <LowerBound>-<UpperBound>\n")
            sys.exit(1)
        randomstring = getRandom(bounds, "intrandom")
        returnTagValue = 'answer=%s' % randomstring
    elif target == "hash":
        # finaltag is the secretstring
        # Concatenate student_lab_instance_seed with secretstring then hash
        string_to_be_hashed = '%s:%s' % (student_lab_instance_seed, finaltag)
        mymd5 = md5.new()
        mymd5.update(string_to_be_hashed)
        newhash = mymd5.hexdigest()
        returnTagValue = 'answer=%s' % newhash

    return returnTagValue

def ValidateTag(studentdir, inputtag, allowed_special_answer):
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
                sys.stderr.write("ERROR: goals.config resulttag (%s) is not allowed 'answer.<string>'\n" % inputtag)
                sys.exit(1)
        returntag = inputtag
    elif '=' in inputtag:
        if not allowed_special_answer:
            sys.stderr.write("ERROR: goals.config only answertag is allowed answer=<string>, resulttag (%s) is not\n" % inputtag)
            sys.exit(1)
        #print "tag %s contains '='" % inputtag
        (target, finaltag) = inputtag.split('=')
        if not (target == "answer" or target == "asciirandom" or
                target == "hexrandom" or target == "intrandom" or target == "hash"):
            sys.stderr.write("ERROR: goals.config tag=<string> then\n")
            sys.stderr.write("       tag must be (answer, asciirandom, hexrandom or intrandom) (%s)\n" % inputtag)
            sys.exit(1)
        # check is done inside generateSpecialTagValue
        returntag = generateSpecialTagValue(studentdir, target, finaltag)
    else:
        #print "tag is %s" % inputtag
        if not inputtag.isalnum():
            sys.stderr.write("ERROR: goals.config contains tag (%s) not alphanumeric\n" % inputtag)
            sys.exit(1)
        returntag = 'result.%s' % inputtag

    return returntag

def ParseGoals(studentdir):
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
                # expecting - <type> : <operator> : <resulttag> : <answertag>
                values = each_value.split(":")
                numvalues = len(values)
                if numvalues != 4:
                    sys.stderr.write("ERROR: goals.config contains unexpected value (%s) format\n" % each_value)
                    sys.exit(1)
                goal_type = values[0].strip()
                goal_operator = values[1].strip()
                resulttag = values[2].strip()
                answertag = values[3].strip()
                # Allowed 'answer=<string>' for answertag only
                valid_answertag = ValidateTag(studentdir, answertag, True)
                valid_resulttag = ValidateTag(studentdir, resulttag, False)
                if not (goal_type == "matchanyany" or
                    goal_type == "matchoneany" or
                    goal_type == "matchonelast"):
                    sys.stderr.write("ERROR: goals.config contains unrecognized type (%s)\n" % goal_type)
                    sys.exit(1)
                if not (goal_operator == "string_equal" or
                    goal_operator == "string_diff" or
                    goal_operator == "string_start" or
                    goal_operator == "string_end" or
                    goal_operator == "integer_equal" or
                    goal_operator == "integer_greater" or
                    goal_operator == "integer_lessthan"):
                    sys.stderr.write("ERROR: goals.config contains unrecognized operator (%s)\n" % goal_operator)
                    sys.exit(1)
                nametags[each_key] = MyGoal(each_key, goal_type, goal_operator, valid_answertag, valid_resulttag)
                #nametags[each_key].toJSON()
                #nametags[each_key].goal_type = goal_type
                #nametags[each_key].goal_operator = goal_operator
                #nametags[each_key].answertag = valid_answertag
                #nametags[each_key].resulttag = valid_resulttag

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

# Usage: GoalsParser.py <studentdir>
# Arguments:
#     <studentdir> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
def main():
    #print "Running GoalsParser.py"
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: GoalsParser.py <studentdir>\n")
        sys.exit(1)

    studentdir = sys.argv[1]
    ParseGoals(studentdir)
    return 0

if __name__ == '__main__':
    sys.exit(main())

