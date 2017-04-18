#!/usr/bin/env python

# ResultParser.py
# Description: * Read results.config
#              * Parse stdin and stdout files based on results.config
#              * Create a json file

import datetime
import json
import glob
import os
import re
import sys
import time
import MyUtil

UBUNTUHOME = "/home/ubuntu/"
logfilelist = []
exec_proglist = []
containernamelist = []
stdinfnameslist = []
stdoutfnameslist = []
timestamplist = {}
nametags = {}
line_types = ['CONTAINS', 'LINE', 'STARTSWITH', 'NEXT_STARTSWITH', 'HAVESTRING', 'LINE_COUNT']
just_field_type = ['LINE_COUNT']
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
    
def ValidateConfigfile(labidname, each_key, each_value):
    valid_field_types = ['TOKEN', 'PARENS', 'QUOTES', 'SLASH', 'LINE_COUNT']
    if not MyUtil.CheckAlphaDashUnder(each_key):
        sys.stderr.write("ERROR: Not allowed characters in results.config's key (%s)\n" % each_key)
        sys.exit(1)
    values = []
    # expecting either:
    # 1. - [ stdin | stdout ] : [<field_type>] : <field_id> :  <line_type1> : <line_id>
    #    field_type = (a valid_field_type defined above)
    #    field_value is a numeric identifying the nth field of the given type
    #    line_type1 = LINE | STARTSWITH | NEXT_STARTSWITH | HAVESTRING
    #    line_id is a number if the type is LINE, or a string if the type is STARTSWITH/HAVESTRING
    # 2. - [ stdin | stdout ] : <line_type2> : <line_id>
    #    line_type2 = CONTAINS
    #    line_id is a string if the type is CONTAINS

    # NOTE: Split using ' : ' - i.e., "space colon space"
    values = [x.strip() for x in each_value.split(' : ')]
    #print values
    numvalues = len(values)
    #print "numvalues is (%d)" % numvalues
    if numvalues < 3 and values[1] not in just_field_type:
        sys.stderr.write("ERROR: results.config contains unexpected value (%s) format\n" % each_value)
        sys.exit(1)
    line_at = findLineIndex(values)
    if line_at is None:
        sys.stderr.write('No line_type in %s\n' % each_value)
        exit(1)
    num_splits = line_at+1
    #print "line_at is (%d) and num_splits is (%d)" % (line_at, num_splits)
     
    # Split into either four or five parts (for line_type1) or three parts (for line_type2)
    # NOTE: Split using ' : ' - i.e., "space colon space"
    values = [x.strip() for x in each_value.split(' : ', num_splits)]

    # Make sure it is 'stdin' or 'stdout'
    newprogname_type = values[0].strip()
    # <cfgcontainername>:<exec_program>.<type>
    if ':' in newprogname_type:
        cfgcontainername, progname_type = newprogname_type.split(':', 1)
    else:
        cfgcontainername = ""
        progname_type = newprogname_type
    # Construct proper containername from cfgcontainername
    if cfgcontainername == "":
        containername = ""
    else:
        containername = labidname + "." + cfgcontainername + ".student"

    if containername != "":
        if containername not in containernamelist:
            containernamelist.append(containername)
    # Use rsplit() here because exec_program may have '.' as part of name
    (exec_program, targetfile) = progname_type.rsplit('.', 1)
    # No longer restricted to stdin/stdout filenames anymore
    if (targetfile != "stdin") and (targetfile != "stdout"):
        # Not stdin/stdout - add the full name
        if progname_type not in logfilelist:
            logfilelist.append(progname_type)
    else:
        if exec_program not in exec_proglist:
            exec_proglist.append(exec_program)
    #    sys.stderr.write("ERROR: results.config line (%s)\n" % each_value)
    #    sys.stderr.write("ERROR: results.config uses not stdin or sdout\n")
    #    sys.exit(1)

    # If line_type1 (line_at != 1) - verify token id
    if line_at != 1:
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
        if field_type not in valid_field_types:
            sys.stderr.write("ERROR: results.config line (%s)\n" % each_value)
            sys.stderr.write("ERROR: results.config invalid field_type\n")
            sys.exit(1)

    return 0

def ParseStdinStdout(studentlabdir, mycontainername, instructordir, labidname):
    configfilename = '%s/.local/instr_config/%s' % (UBUNTUHOME, "results.config")
    configfile = open(configfilename)
    configfilelines = configfile.readlines()
    configfile.close()
    jsonoutputfilename = labidname
    #print "ParseStdinStdout: jsonoutputfilename is (%s)" % jsonoutputfilename
  
    timestamplist[mycontainername] = []
    nametags[mycontainername] = {}
    for line in configfilelines:
        linestrip = line.rstrip()
        if linestrip:
            if not linestrip.startswith('#'):
                #print "Current linestrip is (%s)" % linestrip
                (each_key, each_value) = linestrip.split('=', 1)
                each_key = each_key.strip()
                ValidateConfigfile(labidname, each_key, each_value)
        #else:
        #    print "Skipping empty linestrip is (%s)" % linestrip

    #print "exec_proglist is: "
    #print exec_proglist
    #print "logfilelist is: "
    #print logfilelist

    RESULTHOME = '%s/%s/%s' % (studentlabdir, mycontainername, ".local/result/")
    #print RESULTHOME
    # if directory does not exist, just return
    if not os.path.exists(RESULTHOME):
        return 0
    OUTPUTRESULTHOME = '%s/%s' % (studentlabdir, ".local/result/")
    #print OUTPUTRESULTHOME
    # if directory does not exist, just return
    if not os.path.exists(OUTPUTRESULTHOME):
        os.makedirs(OUTPUTRESULTHOME)
        
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

    # Process line_type1 - i.e., LINE/STARTSWITH/HAVESTRING - artifacts with timestamps
    for timestamppart in timestamplist[mycontainername]:
        outputjsonfname = '%s%s.%s' % (OUTPUTRESULTHOME, jsonoutputfilename, timestamppart)
        #print "ParseStdinStdout (1): Outputjsonfname is (%s)" % outputjsonfname

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
                    # NOTE: Split using ' : ' - i.e., "space colon space"
                    values = [x.strip() for x in each_value.split(' : ')]
                    line_at = findLineIndex(values)
                    num_splits = line_at+1
                    # NOTE: Split using ' : ' - i.e., "space colon space"
                    values = [x.strip() for x in each_value.split(' : ', num_splits)]
                    newtargetfile = values[0].strip()
                    # <cfgcontainername>:<exec_program>.<type>
                    if ':' in newtargetfile:
                        cfgcontainername, targetfile = newtargetfile.split(':', 1)
                    else:
                        cfgcontainername = ""
                        targetfile = newtargetfile
                    # Construct proper containername from cfgcontainername
                    if cfgcontainername == "":
                        containername = ""
                    else:
                        containername = labidname + "." + cfgcontainername + ".student"

                    if containername != "" and mycontainername != containername:
                        #print "Config line (%s) not for my container (%s), skipping..." % (linestrip, mycontainername)
                        # set nametags - value pair to NONE
                        nametags[mycontainername][each_key] = "NONE"
                        continue

                    command = values[line_at].strip()
                    # field_type - if exists (because field_type is optional)
                    #              has been validated to be one of the valid field types.
                    #              
                    # if it does not exists, default field_type is TOKEN
                    if line_at == 3:
                        field_type = values[1].strip()
                    else:
                        field_type = "TOKEN"
                    # command has been validated to be either 'LINE' or 'STARTSWITH' or 'HAVESTRING'
                    token_index = 1
                    if line_at == 3:
                        token_index = 2
                    token_id = values[token_index].strip()
                    if command == 'LINE':
                        lineno = int(values[line_at+1].strip())
                    elif command not in just_field_type:
                        # command = 'STARTSWITH': or 'HAVESTRING'
                        lookupstring = values[line_at+1].strip()

                    targetfname = '%s%s.%s' % (RESULTHOME, targetfile, timestamppart)
                    #print "targetfname is (%s)" % targetfname
                    if not os.path.exists(targetfname):
                        # If file does not exist, treat as can't find token
                        token = "NONE"
                        #sys.stderr.write("ERROR: No %s file does not exist\n" % targetfname)
                        #sys.exit(1)
                    else:
                        # Get the modified time
                        targetmtime = os.path.getmtime(targetfname)
                        #print('target mtime %s' % targetmtime)
                        targetmtime_string = datetime.datetime.fromtimestamp(targetmtime)
                        targetmtime_formatted = targetmtime_string.strftime("%Y%m%d%H%M%S")
                        #print('targetmtime time is %s' % targetmtime_string)
                        #print('targetmtime formatted is %s' % targetmtime_formatted)

                        # Read in corresponding file
                        targetf = open(targetfname, "r")
                        targetlines = targetf.readlines()
                        targetf.close()
                        targetfilelen = len(targetlines)

                        #print "Stdin has (%d) lines" % targetfilelen
                        #print targetlines

                        #print "targetfile is %s" % targetfile
                        # command has been validated to be either 'LINE' or 'STARTSWITH' or 'HAVESTRING'
                        linerequested = "NONE"
                        if command == 'LINE':
                            # make sure lineno <= targetfilelen
                            if lineno <= targetfilelen:
                                linerequested = targetlines[lineno-1]
                        elif command == 'HAVESTRING':
                            # command = 'HAVESTRING':
                            found_lookupstring = False
                            for currentline in targetlines:
                                if found_lookupstring == False:
                                    if lookupstring in currentline:
                                        found_lookupstring = True
                                        linerequested = currentline
                                        break
                            # If not found - set to NONE
                            if found_lookupstring == False:
                                linerequested = "NONE"
                        elif command == 'LINE_COUNT':
                            tagstring = str(targetfilelen)
                            nametags[mycontainername][each_key] = tagstring
                            #print('tag string is %s for eachkey %s' % (tagstring, each_key))
                            continue

                        elif command == 'STARTSWITH':
                            found_lookupstring = False
                            for currentline in targetlines:
                                if found_lookupstring == False:
                                    if currentline.startswith(lookupstring):
                                        found_lookupstring = True
                                        linerequested = currentline
                                        break
                            # If not found - set to NONE
                            if found_lookupstring == False:
                                linerequested = "NONE"
                        elif command == 'NEXT_STARTSWITH':
                            found_lookupstring = False
                            prev_line = None
                            for currentline in targetlines:
                                if found_lookupstring == False:
                                    if currentline.startswith(lookupstring) and prev_line is not None:
                                        found_lookupstring = True
                                        linerequested = prev_line
                                        break
                                prev_line = currentline
                            # If not found - set to NONE
                            if found_lookupstring == False:
                                linerequested = "NONE"
                        else:
                            print('ERROR: unknown command %s' % command)
                            exit(1)

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
                            elif field_type == 'SLASH':
                                myre = linerequested.split('/')
                                linetokenidx = 0
                                for item in myre:
                                    #print "linetokenidx = %d" % linetokenidx
                                    linetokens[linetokenidx] = item
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

        # Got to here - for line_type1, parse for 'PROGRAM FINISH:'
        # If the last line contains 'PROGRAM FINISH'
        #print "targetfilelen = %d" % targetfilelen
        lastline = targetlines[targetfilelen-1].strip()
        #print "lastline = (%s)" % lastline
        if 'PROGRAM FINISH' in targetlines[targetfilelen-1]:
            lastline = targetlines[targetfilelen-1]
            lastlinestrip = lastline.strip()
            lastlinetokens = lastlinestrip.split()
            numlastlinetokens = len(lastlinetokens)
            if numlastlinetokens != 3:
                sys.stderr.write("FATAL: Corrupted PROGRAM FINISH line!\n")
                sys.exit(1)
            else:
                program_end_time = lastlinetokens[2]
        else:
            # No 'PROGRAM FINISH' line - Use the target file modified time
            program_end_time = targetmtime_formatted

        nametags[mycontainername]['PROGRAM_ENDTIME'] = program_end_time


        #print nametags
        jsonoutput = open(outputjsonfname, "w")
        for key in nametags[mycontainername]:
            old = nametags[mycontainername][key]
            new = repr(old)
            nametags[mycontainername][key] = new
        try:
            jsondumpsoutput = json.dumps(nametags[mycontainername], indent=4)
        except:
            print('json dumps failed on %s' % nametags[mycontainername])
            exit(1)
        jsonoutput.write(jsondumpsoutput)
        jsonoutput.write('\n')
        jsonoutput.close()

    # Process line_type2 - i.e., CONTAINS - artifacts without timestamps
    # Output JSON file will not have timestamp either
    outputjsonfname = '%s%s' % (OUTPUTRESULTHOME, jsonoutputfilename)
    #print "ParseStdinStdout (2): Outputjsonfname is (%s)" % outputjsonfname

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
                # NOTE: Split using ' : ' - i.e., "space colon space"
                values = [x.strip() for x in each_value.split(' : ')]
                line_at = findLineIndex(values)

                # Do only line_at == 1
                if line_at != 1 or values[1] in just_field_type:
                    continue

                num_splits = line_at+1
                # NOTE: Split using ' : ' - i.e., "space colon space"
                values = [x.strip() for x in each_value.split(' : ', num_splits)]
                newtargetfile = values[0].strip()
                # <cfgcontainername>:<exec_program>.<type>
                if ':' in newtargetfile:
                    cfgcontainername, targetfile = newtargetfile.split(':', 1)
                else:
                    cfgcontainername = ""
                    targetfile = newtargetfile
                # Construct proper containername from cfgcontainername
                if cfgcontainername == "":
                    containername = ""
                else:
                    containername = labidname + "." + cfgcontainername + ".student"

                if containername != "" and mycontainername != containername:
                    #print "Config line (%s) not for my container (%s), skipping..." % (linestrip, mycontainername)
                    continue

                command = values[line_at].strip()
                # no field_type and no token_id
                containsstring = values[line_at+1].strip()

                targetfname = '%s%s' % (RESULTHOME, targetfile)
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
                    # command has been validated to be 'CONTAINS'
                    found_containsstring = False
                    for currentline in targetlines:
                        if found_containsstring == False:
                            # if current line has the string
                            if containsstring in currentline:
                                found_containsstring = True
                                break

                # If not found - set to False
                if found_containsstring == False:
                    tagstring = "False"
                else:
                    tagstring = "True"

                # set nametags - value pair
                nametags[mycontainername][each_key] = tagstring

        # Got to here - for line_type2, set PROGRAM_ENDTIME as 'NONE'
        nametags[mycontainername]['PROGRAM_ENDTIME'] = "NONE"


# Usage: ResultParser.py <studentlabdir> <mycontainername> <instructordir> <labidname>
# Arguments:
#     <studentlabdir> - directory containing the student lab work
#                    extracted from zip file (done in Instructor.py)
#     <mycontainername> - name of the container
#     <instructordir> - directory containing instructor's solution
#                       for corresponding student
#     <labidname> - name of the lab
def main():
    #print "Running ResultParser.py"
    if len(sys.argv) != 5:
        sys.stderr.write("Usage: ResultParser.py <studentlabdir> <mycontainername> <instructordir> <labidname>\n")
        sys.exit(1)

    studentlabdir = sys.argv[1]
    mycontainername = sys.argv[2]
    instructordir = sys.argv[3]
    labidname = sys.argv[4]
    ParseStdinStdout(studentlabdir, mycontainername, instructordir, labidname)
    return 0

if __name__ == '__main__':
    sys.exit(main())

