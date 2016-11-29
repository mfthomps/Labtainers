#!/usr/bin/env python

# ResultParser.py
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

def ValidateConfigfile(each_key, each_value):
    if not each_key.isalnum():
        sys.stderr.write("ERROR: parser.config contains key (%s) not alphanumeric\n" % each_key)
        sys.exit(1)
    values = []
    # expecting - [ stdin | stdout ] : <command> : <param>
    # If <command> is 'LINE' then <param> is <lineno> : <token>
    # If <command> is 'STARTSWITH' then <param> is <token> : <string>

    # Test split - expecting at least four parts, either:
    # [ stdin | stdout ] : LINE : <lineno> : <token>
    # [ stdin | stdout ] : STARTSWITH : <token> : <string>
    values = each_value.split(':')
    #print values
    numvalues = len(values)
    if numvalues < 4:
        sys.stderr.write("ERROR: parser.config contains unexpected value (%s) format\n" % each_value)
        sys.exit(1)
    values = []
    # Split into four parts - last part will be taken as string if <command> is 'STARTSWITH'
    values = each_value.split(':', 3)

    # Make sure it is 'stdin' or 'stdout'
    progname_type = values[0].strip()
    (exec_program, targetfile) = progname_type.split('.')
    if exec_program not in exec_proglist:
        exec_proglist.append(exec_program)
    if (targetfile != "stdin") and (targetfile != "stdout"):
        sys.stderr.write("ERROR: parser.config line (%s)\n" % each_value)
        sys.stderr.write("ERROR: parser.config uses not stdin or sdout\n")
        sys.exit(1)

    # Make sure command is either 'LINE' or 'STARTSWITH'
    command = values[1].strip()
    if command == 'LINE':
        #print "command is LINE"
        # Make sure lineno is integer - line is next after command 'LINE'
        lineno = values[2].strip()
        #print lineno
        try:
            int(lineno)
        except ValueError:
            sys.stderr.write("ERROR: parser.config line (%s)\n" % each_value)
            sys.stderr.write("ERROR: parser.config has invalid lineno\n")
            sys.exit(1)

        # Make sure tokenno is integer
        tokenno = values[3].strip()
        #print tokenno
        try:
            int(tokenno)
        except ValueError:
            sys.stderr.write("ERROR: parser.config line (%s)\n" % each_value)
            sys.stderr.write("ERROR: parser.config has invalid tokenno\n")
            sys.exit(1)
    elif command == 'STARTSWITH':
        #print "command is STARTSWITH"
        # Make sure tokenno is integer - token is next after command 'STARTSWITH'
        tokenno = values[2].strip()
        #print tokenno
        try:
            int(tokenno)
        except ValueError:
            sys.stderr.write("ERROR: parser.config line (%s)\n" % each_value)
            sys.stderr.write("ERROR: parser.config has invalid tokenno\n")
    else:
        sys.stderr.write("ERROR: parser.config contains unexpected command (%s) format\n" % each_value)
        sys.exit(1)

    return 0

def ParseStdinStdout(studentdir, instructordir, jsonoutfile):
    configfilename = '%s/.local/config/%s' % (UBUNTUHOME, "parser.config")
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
                ValidateConfigfile(each_key, each_value)
        #else:
        #    print "Skipping empty linestrip is (%s)" % linestrip

    #print "exec_proglist is: "
    #print exec_proglist

    RESULTHOME = '%s/%s' % (studentdir, ".local/result/")
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
        
        for line in configfilelines:
            linestrip = line.rstrip()
            if linestrip:
                if not linestrip.startswith('#'):
                    #print "Current linestrip is (%s)" % linestrip
                    (each_key, each_value) = linestrip.split('=', 1)
                    each_key = each_key.strip()

                    #print each_key
                    # Note: config file has been validated
                    values = []
                    # Split into four parts - 
                    # last part will be taken as string if <command> is 'STARTSWITH'
                    values = each_value.split(':', 3)
                    targetfile = values[0].strip()
                    command = values[1].strip()
                    # command has been validated to be either 'LINE' or 'STARTSWITH'
                    if command == 'LINE':
                        lineno = int(values[2].strip())
                        tokenno = int(values[3].strip())
                    else:
                        # command = 'STARTSWITH':
                        tokenno = int(values[2].strip())
                        startstring = values[3].strip()

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
                    # command has been validated to be either 'LINE' or 'STARTSWITH'
                    if command == 'LINE':
                        # make sure lineno <= targetfilelen
                        if lineno > targetfilelen:
                            linerequested = "NONE"
                            #print "setting result to none lineno > stdin length"
                        else:
                            linerequested = targetlines[lineno-1]
                    else:
                        # command = 'STARTSWITH':
                        found_startstring = False
                        for currentline in targetlines:
                            if found_startstring == False:
                                if currentline.startswith(startstring):
                                    found_startstring = True
                                    linerequested = currentline
                                    break
                        # If not found - set to NONE
                        if found_startstring == False:
                            linerequested = "NONE"

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

