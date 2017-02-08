#!/usr/bin/env python

# ResultParser.py
# Description: * Read results.config
#              * Parse stdin and stdout files based on results.config
#              * Create a json file

import json
import glob
import os
import re
import sys
import MyUtil

UBUNTUHOME = "/home/ubuntu/"
exec_proglist = []
containernamelist = []
stdinfnameslist = []
stdoutfnameslist = []
timestamplist = {}
nametags = {}
line_types = ['LINE', 'STARTSWITH']
def ValidateTokenId(each_value, token_id):
    if token_id != 'ALL' and token_id != 'LAST':
        try:
            int(token_id)
        except ValueError:
            sys.stderr.write("ERROR: results.config line (%s)\n" % each_value)
            sys.stderr.write("ERROR: results.config has invalid token_id\n")
            sys.exit(1)

def findLineIndex(values):
    for ltype in line_types:
        if ltype in values:
            return values.index(ltype)
    return None
    
def ValidateConfigfile(each_key, each_value):
    if not MyUtil.CheckAlphaDashUnder(each_key):
        sys.stderr.write("ERROR: Not allowed characters in results.config's key (%s)\n" % each_key)
        sys.exit(1)
    values = []
    # expecting - [ stdin | stdout ] : [<field_type>] : <field_id> :  <line_type> : <line_id>
    #    field_type = TOKEN | PARENS | QUOTES
    #    field_value is a numeric identifying the nth field of the given type
    #    line_type = LINE | STARTSWITH
    #    line_id is a number if the type is LINE, or a string if the tye is STARTSWITH

    values = [x.strip() for x in each_value.split(':')]
    #print values
    numvalues = len(values)
    if numvalues < 4:
        sys.stderr.write("ERROR: results.config contains unexpected value (%s) format\n" % each_value)
        sys.exit(1)
    line_at = findLineIndex(values)
    if line_at is None:
        sys.stderr.write('No line_type in %s\n' % each_value)
        exit(1)
    num_splits = line_at+1
     
    # Split into four or five parts 
    values = [x.strip() for x in each_value.split(':', num_splits)]

    # Make sure it is 'stdin' or 'stdout'
    newprogname_type = values[0].strip()
    # <containername>=<exec_program>.<type>
    if '=' in newprogname_type:
        containername, progname_type = newprogname_type.split('=', 1)
    else:
        containername = ""
        progname_type = newprogname_type
    if containername != "":
        if containername not in containernamelist:
            containernamelist.append(containername)
    # Use rsplit() here because exec_program may have '.' as part of name
    (exec_program, targetfile) = progname_type.rsplit('.', 1)
    if exec_program not in exec_proglist:
        exec_proglist.append(exec_program)
    if (targetfile != "stdin") and (targetfile != "stdout"):
        sys.stderr.write("ERROR: results.config line (%s)\n" % each_value)
        sys.stderr.write("ERROR: results.config uses not stdin or sdout\n")
        sys.exit(1)

    token_index = 1
    if line_at == 3:
        token_index = 2
    ValidateTokenId(each_value, values[token_index])
    if values[line_at] == 'LINE':
        try:
            int(values[line_at+1])
        except:
            sys.stderr.write('Expected integer following LINE type, got %s in %s' % (values[line_at+1], each_value))
            exit(1)

    # Validate <field_type> - if exists (i.e., line_at == 3)
    #                       - because <field_type> is optional
    if line_at == 3:
        field_type = values[1].strip()
        if (field_type != "TOKEN") and (field_type != "PARENS") and (field_type != "QUOTES"):
            sys.stderr.write("ERROR: results.config line (%s)\n" % each_value)
            sys.stderr.write("ERROR: results.config invalid field_type\n")
            sys.exit(1)

    return 0

def ParseStdinStdout(studentlabdir, mycontainername, instructordir, jsonoutputfilename):
    configfilename = '%s/.local/instr_config/%s' % (UBUNTUHOME, "results.config")
    configfile = open(configfilename)
    configfilelines = configfile.readlines()
    configfile.close()
  
    timestamplist[mycontainername] = []
    nametags[mycontainername] = {}
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

    RESULTHOME = '%s/%s/%s' % (studentlabdir, mycontainername, ".local/result/")
    #print RESULTHOME
    for exec_prog in exec_proglist:
        stdinfiles = '%s%s.%s.' % (RESULTHOME, exec_prog, "stdin")
        stdoutfiles = '%s%s.%s.' % (RESULTHOME, exec_prog, "stdout")
        #print stdinfiles
        #print stdoutfiles
        globstdinfnames = glob.glob('%s*' % stdinfiles)
        if globstdinfnames != []:
            #print "globstdinfname list is "
            #print globstdinfnames
            for stdinfnames in globstdinfnames:
                #print stdinfnames
                stdinfnameslist.append(stdinfnames)
        globstdoutfnames = glob.glob('%s*' % stdoutfiles)
        if globstdoutfnames != []:
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
            #print "stdinfiles is %s" % stdinfiles
            if stdinfiles in stdinfname:
                #print "match"
                (filenamepart, timestamppart) = stdinfname.split(stdinfiles)
                if timestamppart not in timestamplist[mycontainername]:
                    timestamplist[mycontainername].append(timestamppart)
            else:
                #print "no match"
                continue

    for timestamppart in timestamplist[mycontainername]:
        outputjsonfname = '%s/%s.%s' % (RESULTHOME, jsonoutputfilename, timestamppart)
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
                    # Split into four parts or five parts
                    values = [x.strip() for x in each_value.split(':')]
                    line_at = findLineIndex(values)
                    num_splits = line_at+1
                    values = [x.strip() for x in each_value.split(':', num_splits)]
                    newtargetfile = values[0].strip()
                    # <containername>=<exec_program>.<type>
                    if '=' in newtargetfile:
                        containername, targetfile = newtargetfile.split('=', 1)
                    else:
                        containername = ""
                        targetfile = newtargetfile
                    if containername != "" and mycontainername != containername:
                        #print "Config line (%s) not for my container (%s), skipping..." % (linestrip, mycontainername)
                        continue

                    command = values[line_at].strip()
                    # field_type - if exists (because field_type is optional)
                    #              has been validated to be either
                    #              'TOKEN' or 'PARENS' or 'QUOTES'
                    # if it does not exists, default field_type is TOKEN
                    if line_at == 3:
                        field_type = values[1].strip()
                    else:
                        field_type = "TOKEN"
                    # command has been validated to be either 'LINE' or 'STARTSWITH'
                    token_index = 1
                    if line_at == 3:
                        token_index = 2
                    token_id = values[token_index].strip()
                    if command == 'LINE':
                        lineno = int(values[line_at+1].strip())
                    else:
                        # command = 'STARTSWITH':
                        startstring = values[line_at+1].strip()

                    targetfname = '%s%s.%s' % (RESULTHOME, targetfile, timestamppart)
                    #print "targetfname is (%s)" % targetfname
                    if not os.path.exists(targetfname):
                        # If file does not exist, treat as can't find token
                        token = "NONE"
                        #sys.stderr.write("ERROR: No %s file does not exist\n" % targetfname)
                        #sys.exit(1)
                    else:
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
                            linetokens = {}
                            if field_type == 'PARENS':
                                myre = re.findall('\(.+?\)', linerequested)
                                linetokenidx = 0
                                for item in myre:
                                    #print "linetokenidx = %d" % linetokenidx
                                    linetokens[linetokenidx] = item[1:-1]
                                    linetokenidx = linetokenidx + 1
                                numlinetokens = len(linetokens)
                            elif field_type == 'QUOTES':
                                myre = re.findall('".+?"', linerequested)
                                linetokenidx = 0
                                for item in myre:
                                    #print "linetokenidx = %d" % linetokenidx
                                    linetokens[linetokenidx] = item[1:-1]
                                    linetokenidx = linetokenidx + 1
                                numlinetokens = len(linetokens)
                            else:
                                # field_type == "TOKEN"
                                linetokens = linerequested.split()
                                numlinetokens = len(linetokens)
                            if token_id == 'ALL':
                                token = linerequested.strip()
                            elif token_id == 'LAST':
                                token = linetokens[numlinetokens-1]
                            else:
                                #print linetokens
                                # make sure tokenno <= numlinetokens
                                tokenno = int(token_id)
                                #print "tokenno = %d" % tokenno
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
                    nametags[mycontainername][each_key] = tagstring

        #print nametags
        jsonoutput = open(outputjsonfname, "w")
        jsondumpsoutput = json.dumps(nametags[mycontainername], indent=4)
        jsonoutput.write(jsondumpsoutput)
        jsonoutput.write('\n')
        jsonoutput.close()

# Usage: ResultParser.py <studentlabdir> <mycontainername> <instructordir> <jsonoutputfilename>
# Arguments:
#     <studentlabdir> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
#     <mycontainername> - name of the container
#     <instructordir> - directory containing instructor's solution
#                       for corresponding student
#     <jsonoutputfilename> - filename for the resulting json file
def main():
    #print "Running ResultParser.py"
    if len(sys.argv) != 5:
        sys.stderr.write("Usage: ResultParser.py <studentlabdir> <mycontainername> <instructordir> <jsonoutputfilename>\n")
        sys.exit(1)

    studentlabdir = sys.argv[1]
    mycontainername = sys.argv[2]
    instructordir = sys.argv[3]
    jsonoutputfilename = sys.argv[4]
    ParseStdinStdout(studentlabdir, mycontainername, instructordir, jsonoutputfilename)
    return 0

if __name__ == '__main__':
    sys.exit(main())

