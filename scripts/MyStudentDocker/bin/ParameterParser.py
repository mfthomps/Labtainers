#!/usr/bin/env python

# ParameterParser.py
# Description: * Read parser.config
#              * Parse stdin and stdout files based on parser.config
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

def CheckRandReplaceEntry(each_value):
    # RAND_REPLACE : <filename> : <token> : <LowerBound> : <UpperBound>
    print "Checking RAND_REPLACE entry"
    entryline = each_value.split(':')
    print entryline
    numentry = len(entryline)
    if numentry != 4:
        sys.stderr.write("ERROR: RAND_REPLACE (%s) improper format\n" % each_value)
        sys.stderr.write("ERROR: RAND_REPLACE : <filename> : <token> : <LowerBound> : <UpperBound>\n")
    myfilename = entryline[0].strip()
    token = entryline[1].strip()
    lowerbound = int(entryline[2].strip())
    upperbound = int(entryline[3].strip())
    print "filename is (%s)" % myfilename
    print "token is (%s)" % token
    print "lowerbound is (%d)" % lowerbound
    print "upperbound is (%d)" % upperbound
    if not os.path.exists(myfilename):
        sys.stderr.write("ERROR: No %s file does not exist\n" % myfilename)
        sys.exit(1)
    else:
        print "File (%s) exist\n" % myfilename


def CheckHashCreateEntry(each_value):
    # HASH_CREATE : <filename> : <string>
    print "Checking HASH_CREATE entry"
    entryline = each_value.split(':')
    print entryline
    numentry = len(entryline)
    if numentry != 2:
        sys.stderr.write("ERROR: RAND_CREATE (%s) improper format\n" % each_value)
        sys.stderr.write("ERROR: HASH_CREATE : <filename> : <string>\n")
    myfilename = entryline[0].strip()
    secretstring = entryline[1].strip()
    print "filename is (%s)" % myfilename
    print "secretstring is (%s)" % secretstring

def CheckHashReplaceEntry(each_value):
    # HASH_REPLACE : <filename> : <token> : <string>
    print "Checking HASH_REPLACE entry"
    entryline = each_value.split(':')
    print entryline
    numentry = len(entryline)
    if numentry != 3:
        sys.stderr.write("ERROR: RAND_REPLACE (%s) improper format\n" % each_value)
        sys.stderr.write("ERROR: HASH_REPLACE : <filename> : <token> : <string>\n")
    myfilename = entryline[0].strip()
    token = entryline[1].strip()
    secretstring = entryline[2].strip()
    print "filename is (%s)" % myfilename
    print "token is (%s)" % token
    print "secretstring is (%s)" % secretstring

def ValidateParameterConfig(each_key, each_value):
    if each_key == "RAND_REPLACE":
        print "RAND_REPLACE"
        CheckRandReplaceEntry(each_value)
    elif each_key == "HASH_CREATE":
        print "HASH_CREATE"
        CheckHashCreateEntry(each_value)
    elif each_key == "HASH_REPLACE":
        print "HASH_REPLACE"
        CheckHashReplaceEntry(each_value)
    else:
        sys.stderr.write("ERROR: Invalid operator %s\n" % each_key)
        sys.exit(1)
    return 0

def ParseParameterConfig(lab_seed):
    configfilename = '%s/.local/config/%s' % (UBUNTUHOME, "parameter.config")
    configfile = open(configfilename)
    configfilelines = configfile.readlines()
    configfile.close()
  
    for line in configfilelines:
        linestrip = line.rstrip()
        if linestrip:
            if not linestrip.startswith('#'):
                #print "Current linestrip is (%s)" % linestrip
                (each_key, each_value) = linestrip.split(':', 1)
                each_key = each_key.strip()
                ValidateParameterConfig(each_key, each_value)
        #else:
        #    print "Skipping empty linestrip is (%s)" % linestrip

# Usage: ParameterParser.py <lab_seed>
# Arguments:
#     <lab_seed> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
def main():
    #print "Running ParameterParser.py"
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: ParameterParser.py <lab_seed>\n")
        sys.exit(1)

    lab_seed = sys.argv[1]
    ParseParameterConfig(lab_seed)
    return 0

if __name__ == '__main__':
    sys.exit(main())

