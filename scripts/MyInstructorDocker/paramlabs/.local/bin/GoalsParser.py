#!/usr/bin/env python

# GoalsParser.py
# Description: * Read goals.config
#              * Create a json file

import ConfigParser
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
    """ Goal - goalid, goaltype, tag1, tag2 """
    goalid = ""
    goaltype = ""
    tag1 = ""
    tag2 = ""

    def goal_dict(object):
        return object.__dict__

    def __init__(self, goalid, goaltype, tag1, tag2):
        self.goalid = goalid
        self.goaltype = goaltype
        self.tag1 = tag1
        self.tag2 = tag2

def ParseGoals():
    configfile = ConfigParser.ConfigParser()
    configfilename = '%s/.local/config/%s' % (UBUNTUHOME, "goals.config")
    configfile.read(configfilename)

    for eachsection in configfile.sections():
        for (each_key, each_value) in configfile.items(eachsection):
             #print each_key
             #print each_value
             if not each_key.isalnum():
                 sys.stderr.write("ERROR: goals.config contains key (%s) not alphanumeric\n" % each_key)
                 sys.exit(1)
             values = []
             # expecting - <type> : <tag1> : <tag2>
             values = each_value.split(":")
             numvalues = len(values)
             if numvalues != 3:
                 sys.stderr.write("ERROR: goals.config contains unexpected value (%s) format\n" % each_value)
                 sys.exit(1)
             goal_type = values[0].strip()
             tag1 = values[1].strip()
             if not tag1.isalnum():
                 sys.stderr.write("ERROR: goals.config contains tag1 (%s) not alphanumeric\n" % tag1)
                 sys.exit(1)
             tag2 = values[2].strip()
             if not tag2.isalnum():
                 sys.stderr.write("ERROR: goals.config contains tag2 (%s) not alphanumeric\n" % tag2)
                 sys.exit(1)
             if not (goal_type != "matchanyany" or
                 goal_type != "matchoneany" or
                 goal_type != "matchonelast"):
                 sys.stderr.write("ERROR: goals.config contains unrecognized type (%s)\n" % goal_type)
                 sys.exit(1)

             nametags[each_key] = MyGoal(each_key, goal_type, tag1, tag2)
             #nametags[each_key].toJSON()
             #nametags[each_key].goal_type = goal_type
             #nametags[each_key].tag1 = tag1
             #nametags[each_key].tag2 = tag2

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

