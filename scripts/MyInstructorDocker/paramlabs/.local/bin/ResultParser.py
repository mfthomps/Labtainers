#!/usr/bin/env python

# ResultParser.py
# Description: * Read parser.config
#              * Parse stdin and stdout files based on parser.config
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

def ValidateConfigfile(each_key, each_value):
    if not each_key.isalnum():
        sys.stderr.write("ERROR: parser.config contains key (%s) not alphanumeric\n" % each_key)
        sys.exit(1)
    values = []
    # expecting - [ stdin | stdout ] : <lineno> : <token> : <type>
    values = each_value.split(':')
    #print values
    numvalues = len(values)
    if numvalues != 4:
        sys.stderr.write("ERROR: parser.config contains unexpected value (%s) format\n" % each_value)
        sys.exit(1)

    # Make sure it is 'stdin' or 'stdout'
    progname_type = values[0].strip()
    (exec_program, targetfile) = progname_type.split('.')
    if exec_program not in exec_proglist:
        exec_proglist.append(exec_program)
    if (targetfile != "stdin") and (targetfile != "stdout"):
        sys.stderr.write("ERROR: parser.config line (%s)\n" % each_value)
        sys.stderr.write("ERROR: parser.config uses not stdin or sdout\n")
        sys.exit(1)

    # Make sure lineno is integer
    lineno = values[1].strip()
    #print lineno
    try:
        int(lineno)
    except ValueError:
        sys.stderr.write("ERROR: parser.config line (%s)\n" % each_value)
        sys.stderr.write("ERROR: parser.config has invalid lineno\n")
        sys.exit(1)

    # Make sure tokenno is integer
    tokenno = values[2].strip()
    #print tokenno
    try:
        int(tokenno)
    except ValueError:
        sys.stderr.write("ERROR: parser.config line (%s)\n" % each_value)
        sys.stderr.write("ERROR: parser.config has invalid tokenno\n")
        sys.exit(1)

    # Make sure type is 'decimal' or 'hexadecimal' or 'string'
    typevalue = values[3].strip()
    #print typevalue
    if (typevalue != "decimal") and (typevalue != "hexadecimal") and (typevalue != 'string'):
        sys.stderr.write("ERROR: parser.config line (%s)\n" % each_value)
        sys.stderr.write("ERROR: parser.config uses not decimal, hexadecimal or string\n")
        sys.exit(1)

    return 0

def ParseStdinStdout(studentdir, instructordir, jsonoutfile):
    configfile = ConfigParser.ConfigParser()
    configfilename = '%s/.local/config/%s' % (UBUNTUHOME, "parser.config")
    configfile.read(configfilename)

    for eachsection in configfile.sections():
        for (each_key, each_value) in configfile.items(eachsection):
             ValidateConfigfile(each_key, each_value)
    #print "exec_proglist is: "
    #print exec_proglist

    RESULTHOME = '%s/%s' % (studentdir, "result/")
    #print RESULTHOME
    for exec_prog in exec_proglist:
        stdinfiles = '%s%s.%s.' % (RESULTHOME, exec_prog, "stdin")
        stdoutfiles = '%s%s.%s.' % (RESULTHOME, exec_prog, "stdout")
        #print stdinfiles
        #print stdoutfiles
        globstdinfnames = glob.glob('%s*' % stdinfiles)
        if globstdinfnames == []:
            sys.stderr.write("ERROR: No %s* file found\n" % stdinfiles)
            sys.exit(1)
        globstdoutfnames = glob.glob('%s*' % stdoutfiles)
        if globstdoutfnames == []:
            sys.stderr.write("ERROR: No %s* file found\n" % stdoutfiles)
            sys.exit(1)
        #print "globstdinfname list is "
        #print globstdinfnames
        for stdinfnames in globstdinfnames:
            #print stdinfnames
            stdinfnameslist.append(stdinfnames)
        #print "stdoutfnameglob list is "
        #print globstdoutfnames
        for stdoutfnames in globstdoutfnames:
            #print stdoutfnames
            stdoutfnameslist.append(stdoutfnames)

    #print "stdinfname list is "
    #print stdinfnameslist
    #for stdinfname in stdinfnameslist:
    #    print "file name is %s" % stdinfname
    #print "stdoutfname list is "
    #print stdoutfnameslist
    #for stdoutfname in stdoutfnameslist:
    #    print "file name is %s" % stdoutfname

    for stdinfname in stdinfnameslist:
        for exec_prog in exec_proglist:
            stdinfiles = '%s%s.%s.' % (RESULTHOME, exec_prog, "stdin")
            stdoutfiles = '%s%s.%s.' % (RESULTHOME, exec_prog, "stdout")
            #print "file name is %s" % stdinfname
            #####print "stdinfiles is %s" % stdinfiles
            if stdinfiles in stdinfname:
                #print "match"
                (filenamepart, timestamppart) = stdinfname.split(stdinfiles)
                if timestamppart not in timestamplist:
                    timestamplist.append(timestamppart)
            else:
                #print "no match"
                continue

    for timestamppart in timestamplist:
        outputjsonfname = '%s/%s.%s' % (RESULTHOME, jsonoutfile, timestamppart)
        #print "Outputjsonfname is (%s)" % outputjsonfname
        
        for eachsection in configfile.sections():
            for (each_key, each_value) in configfile.items(eachsection):
                #print each_key
                # Note: config file has been validated
                values = []
                values = each_value.split(':')
                targetfile = values[0].strip()
                lineno = int(values[1].strip())
                tokenno = int(values[2].strip())
                typevalue = values[3].strip()

                targetfname = '%s%s.%s' % (RESULTHOME, targetfile, timestamppart)
                #print "targetfname is (%s)" % targetfname
                if not os.path.exists(targetfname):
                    sys.stderr.write("ERROR: No %s file does not exist\n" % targetfname)
                    sys.exit(1)

                # Read in corresponding file
                targetf = open(targetfname, "r")
                targetlines = targetf.readlines()
                targetf.close()
                targetfilelen = len(targetlines)

                #print "Stdin has (%d) lines" % targetfilelen
                #print targetlines

                #print "targetfile is %s" % targetfile
                # make sure lineno <= targetfilelen
                if lineno > targetfilelen:
                    linerequested = "NONE"
                    #print "setting result to none lineno > stdin length"
                else:
                    linerequested = targetlines[lineno-1]

                #print "Line requested is (%s)" % linerequested
                if linerequested == "NONE":
                    token = "NONE"
                else:
                    linetokens = linerequested.split()
                    numlinetokens = len(linetokens)
                    #print linetokens
                    # make sure tokenno <= numlinetokens
                    if tokenno > numlinetokens:
                        token = "NONE"
                        #print "setting result to none tokenno > numlinetokens"
                    else:
                        token = linetokens[tokenno-1]

                #print token
                if token == "NONE":
                    tagstring = "NONE"
                else:
                    # Need to convert token according to typevalue
                    tagstring = token
    
                # set nametags - value pair
                nametags[each_key] = tagstring

        #print nametags
        jsonoutput = open(outputjsonfname, "w")
        jsondumpsoutput = json.dumps(nametags, indent=4)
        jsonoutput.write(jsondumpsoutput)
        jsonoutput.write('\n')
        jsonoutput.close()

# Usage: ResultParser.py <studentdir> <instructordir> <outputjsonfilename>
# Arguments:
#     <studentdir> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
#     <instructordir> - directory containing instructor's solution
#                       for corresponding student
#     <outputjsonfilename> - filename for the resulting json file
def main():
    #print "Running ResultParser.py"
    if len(sys.argv) != 4:
        sys.stderr.write("Usage: ResultParser.py <studentdir> <instructordir> <outputjsonfilename>\n")
        sys.exit(1)

    studentdir = sys.argv[1]
    instructordir = sys.argv[2]
    jsonoutputfilename = sys.argv[3]
    ParseStdinStdout(studentdir, instructordir, jsonoutputfilename)
    return 0

if __name__ == '__main__':
    sys.exit(main())

