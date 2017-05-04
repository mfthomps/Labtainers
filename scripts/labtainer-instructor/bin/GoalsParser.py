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
'''
  GoalsParser.py
  Description: * Read goals.config and create the goals.json file
               * with values specific to this student (parameterized).
'''
import json
import glob
import md5
import os
import random
import sys
import MyUtil
import ParameterParser

UBUNTUHOME = "/home/ubuntu/"
answer_tokens=['result', 'parameter', 'parameter_ascii']
class MyGoal(object):
    """ Goal - goalid, goaltype, goaloperator, answertag, resulttag, boolean_string, goal1tag, goal2tag """
    goalid = ""
    goaltype = ""
    goaloperator = ""
    answertag = ""
    resulttag = ""
    boolean_string = ""
    goal1tag = ""
    goal2tag = ""

    def goal_dict(object):
        return object.__dict__

    def __init__(self, goalid, goaltype, goaloperator="", answertag="", 
                 resulttag="", boolean_string="", goal1tag="", goal2tag=""):
        self.goalid = goalid
        self.goaltype = goaltype
        self.goaloperator = goaloperator
        self.answertag = answertag
        self.resulttag = resulttag
        self.boolean_string = boolean_string
        self.goal1tag = goal1tag
        self.goal2tag = goal2tag

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

def getTagValue(parameter_list, target, finaltag):
    if target == "answer":
        returnTagValue = 'answer=%s' % finaltag
    else:
        if target.startswith('parameter'):
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
        else:
            returnTagValue = '%s.%s' % (target, finaltag)
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

def ValidateTag(parameter_list, studentdir, goal_type, inputtag, allowed_special_answer):
    # if allowed_special_answer is true, then allow 'answer=<string>'
    # UNLESS if the goal_type is matchacross
    returntag = ""
    if '=' in inputtag:
        if not allowed_special_answer:
            sys.stderr.write("ERROR: goals.config only answertag is allowed answer=<string>, resulttag (%s) is not\n" % inputtag)
            sys.exit(1)
        if goal_type == "matchacross":
            sys.stderr.write("ERROR: goals.config answer=<string> and goal_type==matchacross is not allowed\n")
            sys.exit(1)
        (target, finaltag) = inputtag.split('=')
        returntag = getTagValue(parameter_list, target, finaltag)

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

        returntag = getTagValue(parameter_list, target, finaltag)
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
    nametags = []
    configfilename = '%s/.local/instr_config/%s' % (UBUNTUHOME, "goals.config")
    configfile = open(configfilename)
    configfilelines = configfile.readlines()
    configfile.close()
    lab_instance_seed = GetLabInstanceSeed(studentdir)
    param_filename = os.path.join(UBUNTUHOME, '.local', 'config',
          'parameter.config')
    parameter_list = {}
    parameter_list = ParameterParser.ParseParameterConfig(lab_instance_seed,
       param_filename)

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
                # <type> : <goal1tag> : <goal2tag>
                # <type> : <string>
                values = each_value.split(" : ")
                numvalues = len(values)
                if not (numvalues == 4 or numvalues == 3 or numvalues == 2):
                    sys.stderr.write("ERROR: goals.config contains unexpected value (%s) format\n" % each_value)
                    sys.exit(1)
                if numvalues == 4:
                    ''' <type> : <operator> : <resulttag> : <answertag> '''
                    goal_type = values[0].strip()
                    goal_operator = values[1].strip()
                    resulttag = values[2].strip()
                    answertag = values[3].strip()
                    # Allowed 'answer=<string>' for answertag only
                    valid_answertag = ValidateTag(parameter_list, studentdir, goal_type, answertag, True)
                    valid_resulttag = ValidateTag(parameter_list, studentdir, goal_type, resulttag, False)
                    if not (goal_type == "matchany" or
                        goal_type == "matchlast" or
                        goal_type == "matchacross"):
                        sys.stderr.write("ERROR: goals.config contains unrecognized type (1) (%s)\n" % goal_type)
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
                    nametags.append(MyGoal(each_key, goal_type, goaloperator=goal_operator, answertag=valid_answertag, resulttag=valid_resulttag))
                    #print "goal_type non-boolean"
                    #print nametags[each_key].goal_dict()
                elif numvalues == 3:
                    ''' <type> : <goal1tag> : <goal2tag> '''
                    goal_type = values[0].strip()
                    if goal_type == 'time_before' or goal_type == 'time_during':
                        goal1tag = values[1].strip()
                        goal2tag = values[2].strip()
                        nametags.append(MyGoal(each_key, goal_type, goal1tag=goal1tag, goal2tag=goal2tag))
                    elif goal_type == 'count_greater':
                        answertag = values[1].strip()
                        subgoal_list = values[2].strip()
                        nametags.append(MyGoal(each_key, goal_type, answertag=answertag, boolean_string=subgoal_list))
                    else:
                        print('ERROR: could not parse goals.config line %s' % each_value)
                        exit(1)
                    #print "goal_type non-boolean"
                    #print nametags[each_key].goal_dict()
                else:
                    ''' <type> : <string> '''
                    goal_type = values[0].strip()
                    if goal_type == 'boolean':
                        boolean_string = values[1].strip()
                        nametags.append(MyGoal(each_key, goal_type, boolean_string=boolean_string))
                    elif goal_type == 'is_true' or goal_type == 'is_false':
                        resulttag = values[1].strip()
                        #print('parsegoals type is %s result %s' % (goal_type, resulttag))
                        nametags.append(MyGoal(each_key, goal_type, resulttag=resulttag))
                    else:
                        print('ERROR: could not parse goals.config line %s' % s)
                        exit(1)
       
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
    student_parent_dir = os.path.dirname(studentdir)
    resultsdir = os.path.join(student_parent_dir, '.local','result')
    try:
        os.makedirs(resultsdir)
    except:
        pass
    outputjsonfname = os.path.join(resultsdir,'goals.json')
    #print "GoalsParser: Outputjsonfname is (%s)" % outputjsonfname
        
    #print nametags
    jsonoutput = open(outputjsonfname, "w")
    jsondumpsoutput = json.dumps([x.goal_dict() for x in nametags], indent=4)
    jsonoutput.write(jsondumpsoutput)
    jsonoutput.write('\n')
    jsonoutput.close()

    return parameter_list

# Usage: GoalsParser.py <studentdir>
# Arguments:
#     <studentdir> - directory containing the student lab work
#                    extracted from zip file (done in instructor.py)
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

