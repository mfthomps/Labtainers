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
import MyUtil
import ParameterParser

UBUNTUHOME = "/home/ubuntu/"
exec_proglist = []
stdinfnameslist = []
stdoutfnameslist = []
timestamplist = []
nametags = {}
global parameter_list
parameter_list = None
answer_tokens=['result', 'parameter', 'parameter_ascii']
class MyGoal(object):
    """ Goal - goalid, goaltype, goaloperator, answertag, resulttag, boolean_string """
    goalid = ""
    goaltype = ""
    goaloperator = ""
    answertag = ""
    resulttag = ""
    boolean_string = ""

    def goal_dict(object):
        return object.__dict__

    def __init__(self, goalid, goaltype, goaloperator, answertag, resulttag, boolean_string):
        self.goalid = goalid
        self.goaltype = goaltype
        self.goaloperator = goaloperator
        self.answertag = answertag
        self.resulttag = resulttag
        self.boolean_string = boolean_string

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

def getTagValue(target, finaltag):
    global parameter_list
    if target == "answer":
        returnTagValue = 'answer=%s' % finaltag
    else:
        if finaltag not in parameter_list:
            print('Could not find parameter %s' % finaltag)
            exit(1)
        value = parameter_list[finaltag]
        if target.lower() == "parameter_ascii":
            if '0x' in value:
                num = int(value, 16)
            else: 
                num = int(value)
            if num not in range(41, 177):
                print('parameter_ascii value %s not in ascii range' % value)
                exit(1)
            value = chr(num)
        returnTagValue = 'answer=%s' % value
    return returnTagValue

def generateSpecialTagValue(studentdir, target, finaltag):
    STUDENT_LAB_INSTANCE_SEED = '%s/%s' % (studentdir, ".local/.seed")
    student_lab_instance_seedfile = open(STUDENT_LAB_INSTANCE_SEED, 'r')
    student_lab_instance_seed = student_lab_instance_seedfile.read().strip()
    student_lab_instance_seedfile.close()
    #print "Student Lab instance seed is (%s)" % student_lab_instance_seed
    
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
    # if allowed_special_answer is true, then allow 'answer=<string>'
    returntag = ""
    if '=' in inputtag:
        if not allowed_special_answer:
            sys.stderr.write("ERROR: goals.config only answertag is allowed answer=<string>, resulttag (%s) is not\n" % inputtag)
            sys.exit(1)
        (target, finaltag) = inputtag.split('=')
        returntag = getTagValue(target, finaltag)

    elif '.' in inputtag:
        #print "tag %s contains '.'" % inputtag
        (target, finaltag) = inputtag.split('.')
        if not target in answer_tokens:
            sys.stderr.write("ERROR: goals.config tag=<string> then\n")
            sys.stderr.write("       tag must be:(%s), got %s\n" % (','.join(answer_tokens), inputtag))
            sys.exit(1)
        if not MyUtil.CheckAlphaDashUnder(finaltag):
            sys.stderr.write("ERROR: Not allowed characters in goals.config's tag (%s)\n" % inputtag)
            sys.exit(1)

        returntag = getTagValue(target, finaltag)
    else:
        #print "tag is %s" % inputtag
        if not MyUtil.CheckAlphaDashUnder(inputtag):
            sys.stderr.write("ERROR: Not allowed characters in goals.config's tag (%s)\n" % inputtag)
            sys.exit(1)
        returntag = 'result.%s' % inputtag

    return returntag

def GetLabInstanceSeed(studentdir):
    seed_dir = os.path.join(studentdir, ".local",".seed")
    student_lab_instance_seed = None
    with open(seed_dir) as fh:
        student_lab_instance_seed = fh.read().strip()
    if student_lab_instance_seed is None:
        print('could not get lab instance seed from %s' % seed_dir)
        exit(1)
    return student_lab_instance_seed

def ParseGoals(studentdir):
    configfilename = '%s/.local/instr_config/%s' % (UBUNTUHOME, "goals.config")
    configfile = open(configfilename)
    configfilelines = configfile.readlines()
    configfile.close()
    lab_instance_seed = GetLabInstanceSeed(studentdir)
    param_filename = os.path.join(UBUNTUHOME, '.local', 'config',
          'parameter.config')
    global parameter_list
    parameter_list = ParameterParser.ParseParameterConfig(lab_instance_seed,
       "CalledByInstructor", param_filename)

    for line in configfilelines:
        linestrip = line.rstrip()
        if linestrip:
            if not linestrip.startswith('#'):
                #print "Current linestrip is (%s)" % linestrip
                (each_key, each_value) = linestrip.split('=', 1)
                each_key = each_key.strip()
                #print each_key
                #print each_value
                if not MyUtil.CheckAlphaDashUnder(each_key):
                    sys.stderr.write("ERROR: Not allowed characters in goals.config's key (%s)\n" % each_key)
                    sys.exit(1)
                values = []
                # expecting - either:
                # <type> : <operator> : <resulttag> : <answertag>
                # <type> : <string>
                values = each_value.split(":")
                numvalues = len(values)
                if not (numvalues == 4 or numvalues == 2):
                    sys.stderr.write("ERROR: goals.config contains unexpected value (%s) format\n" % each_value)
                    sys.exit(1)
                if numvalues == 4:
                    goal_type = values[0].strip()
                    goal_operator = values[1].strip()
                    resulttag = values[2].strip()
                    answertag = values[3].strip()
                    # Allowed 'answer=<string>' for answertag only
                    valid_answertag = ValidateTag(studentdir, answertag, True)
                    valid_resulttag = ValidateTag(studentdir, resulttag, False)
                    if not (goal_type == "matchanyany" or
                        goal_type == "matchoneany" or
                        goal_type == "matchonelast" or
                        goal_type == "boolean_set"):
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
                    boolean_string = ""
                    nametags[each_key] = MyGoal(each_key, goal_type, goal_operator, valid_answertag, valid_resulttag, boolean_string)
                    #print "goal_type non-boolean"
                    #print nametags[each_key].goal_dict()
                else:
                    goal_type = values[0].strip()
                    boolean_string = values[1].strip()
                    goal_operator = ""
                    valid_resulttag = ""
                    valid_answertag = ""
                    nametags[each_key] = MyGoal(each_key, goal_type, goal_operator, valid_answertag, valid_resulttag, boolean_string)
                    #print "goal_type boolean"
                    #print nametags[each_key].goal_dict()
                #nametags[each_key].toJSON()
                #nametags[each_key].goal_type = goal_type
                #nametags[each_key].goal_operator = goal_operator
                #nametags[each_key].answertag = valid_answertag
                #nametags[each_key].resulttag = valid_resulttag
                #nametags[each_key].boolean_string = boolean_string

        #else:
        #    print "Skipping empty linestrip is (%s)" % linestrip


    #print nametags["crash"].toJSON()
    #for (each_key, each_goal) in nametags.items():
    #    print nametags[each_key].toJSON()
    outputjsonfname = '%s/.local/instr_config/%s' % (UBUNTUHOME, "goals.json")
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

