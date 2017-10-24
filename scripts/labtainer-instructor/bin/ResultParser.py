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
from parse import *

MYHOME = ""
logfilelist = []
container_exec_proglist = {}
containernamelist = []
stdinfnameslist = []
stdoutfnameslist = []
timestamplist = {}
line_types = ['CONTAINS', 'LINE', 'STARTSWITH', 'NEXT_STARTSWITH', 'HAVESTRING', 
              'LINE_COUNT', 'PARAM', 'STRING_COUNT']
just_field_type = ['LINE_COUNT']
logger = None
resultidlist = []

def GetExecProgramList(containername, studentlabdir, container_list, targetfile):
    # This will return a list of executable program name matching
    # <directory>/.local/result/<exec_program>.targetfile.*
    # If containername is "" then loop through all directory of studentlabdir/container
    # where container is from the container_list
    # If containername is non "" then directory is studentlabdir/containername
    myexec_proglist = []
    mylist = []
    if containername == "":
        #print "containername is empty - do for all container in the container list"
        mylist = container_list
    else:
        #print "containername is non empty - do for that container only"
        mylist.append(containername)
    #print "Final container list is "
    #print mylist
    for cur_container in mylist:
        string_to_glob = "%s/%s/.local/result/*.%s.*" % (studentlabdir, cur_container, targetfile)
        #print "string_to_glob is (%s)" % string_to_glob
        globnames = glob.glob('%s' % string_to_glob)
        for name in globnames:
            basefilename = os.path.basename(name)
            #print "basefilename is %s" % basefilename
            split_string = ".%s" % targetfile
            #print "split_string is %s" % split_string
            namesplit = basefilename.split(split_string)
            #print namesplit
            if namesplit[0] not in myexec_proglist:
                myexec_proglist.append(namesplit[0])
    return myexec_proglist


def ValidateTokenId(each_value, token_id, logger):
    if token_id != 'ALL' and token_id != 'LAST':
        try:
            int(token_id)
        except ValueError:
            logger.ERROR("results.config line (%s)\n" % each_value)
            logger.ERROR("results.config has invalid token_id\n")
            sys.exit(1)

def findLineIndex(values):
    for ltype in line_types:
        if ltype in values:
            return values.index(ltype)

    return None

def ValidateConfigfile(actual_parsing, studentlabdir, container_list, labidname, each_key, each_value, logger):
    '''
    Misleading name, this function populates a set of global structures used in processign the results
    '''
    valid_field_types = ['TOKEN', 'PARENS', 'QUOTES', 'SLASH', 'LINE_COUNT', 'CONTAINS', 
                         'SEARCH', 'PARAM', 'STRING_COUNT']
    if not MyUtil.CheckAlphaDashUnder(each_key):
        logger.ERROR("Not allowed characters in results.config's key (%s)\n" % each_key)
        sys.exit(1)
    values = []
    # expecting:
    # . - [ stdin | stdout | prgout ] : [<field_type>] : <field_id> :  <line_type1> : <line_id>
    #    field_type = (a valid_field_type defined above)
    #    field_value is a numeric identifying the nth field of the given type
    #    line_type1 = LINE | STARTSWITH | NEXT_STARTSWITH | HAVESTRING
    #    line_id is a number if the type is LINE, or a string if the type is STARTSWITH/HAVESTRING
    #    line_id is a string if the type is CONTAINS

    # NOTE: Split using ' : ' - i.e., "space colon space"
    values = [x.strip() for x in each_value.split(' : ')]
    #print values
    numvalues = len(values)
    logger.DEBUG("each_value is %s -- numvalues is (%d)" % (each_value, numvalues))
    if numvalues < 3 and values[1] not in just_field_type:
        logger.ERROR("results.config contains unexpected value (%s) format\n" % each_value)
        sys.exit(1)
    line_at = findLineIndex(values)
    if line_at is None:
        logger.ERROR('No line_type in %s\n' % each_value)
        sys.exit(1)
    num_splits = line_at+1
    #print "line_at is (%d) and num_splits is (%d)" % (line_at, num_splits)
     
    # NOTE: Split using ' : ' - i.e., "space colon space"
    values = [x.strip() for x in each_value.split(' : ', num_splits)]

    # get optional container name and determine if it is 'stdin' or 'stdout'
    newprogname_type = values[0].strip()
    logger.DEBUG('newprogname_type is %s' % newprogname_type)
    # <cfgcontainername>:<exec_program>.<type>
    if ':' in newprogname_type:
        cfgcontainername, progname_type = newprogname_type.split(':', 1)
    else:
        if len(container_list) > 1:
            logger.ERROR('No container name found in multi container lab entry: %s' % newprogname_type)
            sys.exit(1)
        if newprogname_type.endswith('stdin') or newprogname_type.endswith('stdout') \
             or newprogname_type.endswith('prgout'):
            cfgcontainername = container_list[0].split('.')[1]
            #print('assigned to %s' % cfgcontainername)
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

    logger.DEBUG('Start to populate exec_program_list, progname_type is %s' % progname_type)
    # No longer restricted to stdin/stdout filenames anymore
    if ('stdin' not in progname_type) and ('stdout' not in progname_type) and ('prgout' not in progname_type):
        # Not stdin/stdout - add the full name
        logger.DEBUG('Not a STDIN or STDOUT: %s ' % progname_type)
        if progname_type not in logfilelist:
            logfilelist.append(progname_type)
    else:
        (exec_program, targetfile) = progname_type.rsplit('.', 1)
        exec_program_list = []
        # Can only parse for wildcard if it is actual parsing - not validation
        if exec_program == "*" and actual_parsing:
            exec_program_list = GetExecProgramList(containername, studentlabdir, container_list, targetfile)
            logger.DEBUG("wildcard, exec_program_list is %s" % exec_program_list)
        else:
            exec_program_list.append(exec_program)
            logger.DEBUG('exec_program %s, append to list, container is %s' % (exec_program, containername))
        if containername != "":
            #print('containername is %s' % containername)
            if containername not in container_exec_proglist:
                container_exec_proglist[containername] = []
            for cur_exec_program in exec_program_list:
                if cur_exec_program not in container_exec_proglist[containername]:
                    container_exec_proglist[containername].append(cur_exec_program)
            logger.DEBUG('proglist is %s' %  str(container_exec_proglist[containername]))
        else:
            if "CURRENT" not in container_exec_proglist:
                container_exec_proglist["CURRENT"] = []
            for cur_exec_program in exec_program_list:
                if cur_exec_program not in container_exec_proglist["CURRENT"]:
                    container_exec_proglist["CURRENT"].append(cur_exec_program)
            #print container_exec_proglist["CURRENT"]

        #print container_exec_proglist

    # Validate <field_type> - if exists (i.e., line_at == 3)
    #                       - because <field_type> is optional
    field_type = None
    if line_at == 3:
        field_type = values[1].strip()
        if field_type not in valid_field_types:
            logger.ERROR("results.config line (%s)\n" % each_value)
            logger.ERROR("results.config invalid field_type\n")
            sys.exit(1)

    # If line_type1 (line_at != 1) - verify token id
    if field_type != 'SEARCH' and line_at != 1:
        token_index = 1
        if line_at == 3:
            token_index = 2
        ValidateTokenId(each_value, values[token_index], logger)

    if values[line_at] == 'LINE':
        try:
            int(values[line_at+1])
        except:
            logger.ERROR('Expected integer following LINE type, got %s in %s' % (values[line_at+1], each_value))
            sys.exit(1)


    return 0

def getToken(linerequested, field_type, token_id, logger):
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
            elif field_type == 'SEARCH':
                logger.DEBUG('is search')
                search_results = search(token_id, linerequested)
                if search_results is not None:
                    token = str(search_results[0])
                else: 
                    token = None
            else:
                # field_type == "TOKEN"
                linetokens = linerequested.split()
                numlinetokens = len(linetokens)


            if token_id == 'ALL':
                token = linerequested.strip()
            elif token_id == 'LAST':
                if numlinetokens > 0:
                    token = linetokens[numlinetokens-1]
                else:
                    token = None
            elif field_type != 'SEARCH':
                #print linetokens
                # make sure tokenno <= numlinetokens
                tokenno = int(token_id)
                #print "tokenno = %d" % tokenno
                if tokenno > numlinetokens:
                    token = "NONE"
                    #print "setting result to none tokenno > numlinetokens"
                else:
                    token = linetokens[tokenno-1]
        return token

def handleConfigFileLine(labidname, line, nametags, studentlabdir, container_list, timestamppart, logger):
    retval = True
    targetlines = None
    #print('line is %s' % line)
    logger.DEBUG('line is %s' % line)
    (each_key, each_value) = line.split('=', 1)
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
    logger.DEBUG('line_at is %d newtargetvalue = %s, values: %s' % (line_at, newtargetfile, str(values)))
    #print('newtargetfile is %s' % newtargetfile)
    # <cfgcontainername>:<exec_program>.<type>
    containername = None
    if ':' in newtargetfile:
        cfgcontainername, targetfile = newtargetfile.split(':', 1)
    else:
        ''' default to first container? '''
        #print('first cont is %s' % container_list[0])
        containername = container_list[0]
        targetfile = newtargetfile
    # Construct proper containername from cfgcontainername
    if containername is None:
        containername = labidname + "." + cfgcontainername + ".student"
    result_home = '%s/%s/%s' % (studentlabdir, containername, ".local/result/")

    if targetfile.startswith('/'):
        targetfile = os.path.join(result_home, targetfile[1:])
    #print('targetfile is %s containername is %s' % (targetfile, containername))
    logger.DEBUG('targetfile is %s, containername is %s' % (targetfile, containername))
    if containername is not None and containername not in container_list:
        print "Config line (%s) containername %s not in container list (%s), skipping..." % (line, containername, str(container_list))
        logger.DEBUG("Config line (%s) containername %s not in container list (%s), skipping..." % (line, 
              containername, str(container_list)))
        # set nametags - value pair to NONE
        #nametags[mycontainername][each_key] = "NONE"
        nametags[each_key] = "NONE"
        return False

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
    if command == 'PARAM':
        token_id = values[2].strip()
    else:
        token_id = values[token_index].strip()
    if command == 'LINE':
        lineno = int(values[line_at+1].strip())
    elif command not in just_field_type:
        # command = 'STARTSWITH': or 'HAVESTRING'
        lookupstring = values[line_at+1].strip()
    logger.DEBUG('command %s, field_type %s, token_id %s' % (command, field_type, token_id))
    targetfname_list = []
    if targetfile.startswith('*'):
        # Handle 'asterisk' -- 
        #print "Handling asterisk"
        #print "containername is %s, targetfile is %s" % (containername, targetfile)
        # Replace targetfile as a list of files
        targetfileparts = targetfile.split('.')
        targetfilestdinstdout = None
        if targetfileparts is not None:
            targetfilestdinstdout = targetfileparts[1]
        if targetfilestdinstdout is not None:
            #print "targetfilestdinstdout is %s" % targetfilestdinstdout
            if containername in container_exec_proglist:
                myproglist = container_exec_proglist[containername]
            else:
                myproglist = container_exec_proglist["CURRENT"]
            for progname in myproglist:
                if timestamppart is not None:
                    targetfname = '%s%s.%s.%s' % (result_home, progname, targetfilestdinstdout, timestamppart)
                    targetfname_list.append(targetfname)
    else:
        #print "Handling non-asterisk"

        if timestamppart is not None:
            targetfname = '%s%s.%s' % (result_home, targetfile, timestamppart)
        else:
            ''' descrete file, no timestamp. '''
            if targetfile.startswith('~/'):
                targetfile = targetfile[2:]
            targetfname = os.path.join(studentlabdir, containername, targetfile)
        #print "targetfname is (%s)" % targetfname
        #print "labdir is (%s)" % studentlabdir

        targetfname_list.append(targetfname)

    #print "Current targetfname_list is %s" % targetfname_list

    tagstring = "NONE"
    # Loop through targetfname_list
    for current_targetfname in targetfname_list:
        if not os.path.exists(current_targetfname):
            # If file does not exist, treat as can't find token
            token = "NONE"
            logger.DEBUG("No %s file does not exist\n" % current_targetfname)
            nametags[each_key] = token
            return False
        else:
            # Read in corresponding file
            targetf = open(current_targetfname, "r")
            targetlines = targetf.readlines()
            targetf.close()
            targetfilelen = len(targetlines)
            #print('current_targetfname %s' % current_targetfname)

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
                nametags[each_key] = targetfilelen
                return True
            elif command == 'PARAM':
                fname = os.path.basename(current_targetfname).rsplit('.',1)[0] 
                if fname.endswith('stdin'):
                    program_name = current_targetfname.rsplit('.', 1)[0]
                else:
                    logger.ERROR('PARAM only valid for stdin files: %s' % current_targetfname)
                    sys.exit(1) 
                if 'PROGRAM_ARGUMENTS' in targetlines[0]:
                    try:
                        index = int(token_id) 
                    except:
                        logger.ERROR('could not parse int from %s' % token_id)
                        sys.exit(1)
                    if index == 0:
                        tagstring = program_name
                    else:
                        s = targetlines[0]
                        param_str = s[s.find("(")+1:s.find(")")]
                        params = param_str.split()
                        try:
                            tagstring = params[index-1]
                        except:
                            logger.ERROR('did not find parameter %d in %s' % (index-1, param_str))
                            sys.exit(1)
                    nametags[each_key] = tagstring
                    return True
            elif command == 'CONTAINS':
                if token_id == 'CONTAINS':
                    ''' search entire file, vice searching for line '''
                    remain = line.split(command,1)[1]
                    remain = remain.split(':', 1)[1].strip()
                    tagstring = 'False'
                    for currentline in targetlines:
                        #print('look for <%s> in %s' % (remain, currentline))
                        if remain in currentline:
                            tagstring = 'True'
                            break 
                    nametags[each_key] = tagstring
                    #print('tag string is %s for eachkey %s' % (tagstring, each_key))
                    return True
                else:
                    # this is deprecated, HAVSTRING should be used
                    found_lookupstring = False
                    for currentline in targetlines:
                        if found_lookupstring == False:
                            if lookupstring in currentline:
                                found_lookupstring = True
                                linerequested = currentline
                                #print('line requested is %s' % linerequested)
                                break
                    # If not found - set to NONE
                    if found_lookupstring == False:
                        linerequested = "NONE"

            elif command == 'STRING_COUNT':
                ''' search entire file, vice searching for line '''
                remain = line.split(command,1)[1]
                remain = remain.split(':', 1)[1].strip()
                count=0
                for currentline in targetlines:
                    #print('look for <%s> in %s' % (remain, currentline))
                    if remain in currentline:
                        count += 1
                nametags[each_key] = count
                #print('tag string is %s for eachkey %s' % (tagstring, each_key))
                return True

            elif command == 'STARTSWITH':
                #print('is startswith')
                found_lookupstring = False
                for currentline in targetlines:
                    if found_lookupstring == False:
                        if currentline.startswith(lookupstring):
                            found_lookupstring = True
                            linerequested = currentline
                            #print('line requested is %s' % linerequested)
                            break
                # If not found - set to NONE
                if found_lookupstring == False:
                    logger.DEBUG('*** No line starts with %s ***' % (lookupstring))
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
                    logger.DEBUG('*** No next line starts with %s ***' % (lookupstring))
                    linerequested = "NONE"
            else:
                logger.ERROR('unknown command %s' % command)
                sys.exit(1)

            token = getToken(linerequested, field_type, token_id, logger)
            logger.DEBUG('field_type %s, token_id %s, got token %s' % (field_type, token_id, token))

        #print token
        if token == "NONE":
            tagstring = "NONE"
        else:
            tagstring = token
            # found the token - break out of the main for loop
            break

    # set nametags - value pair
    nametags[each_key] = tagstring
    return True


def ParseConfigForFile(studentlabdir, labidname, configfilelines, 
                       outputjsonfname, container_list, timestamppart, end_time, logger):
    '''
    Invoked for each timestamp to parse results for that timestamp.
    Each config file line is assessed against each results file that corresponds
    to the given timestamp.  If timestamp is None, then look at all files that
    match the name found in the configuration file line, (e.g., for log files
    without timestamps.)
    '''
    #print('in ParseConfigForFile outputjsonfile: %s timestamppart %s' % (outputjsonfname, timestamppart))
    nametags = {}
    got_one = False
    for line in configfilelines:
        linestrip = line.rstrip()
        if linestrip is not None and not linestrip.startswith('#') and len(line.strip())>0:
            got_one = got_one | handleConfigFileLine(labidname, linestrip, nametags, studentlabdir, container_list, timestamppart, logger)

    if end_time is not None:
        program_end_time = end_time
    else:
        program_end_time = 'NONE'
    if got_one:
        nametags['PROGRAM_ENDTIME'] = program_end_time
        #print nametags
        #print('will dump to %s' % outputjsonfname)
        jsonoutput = open(outputjsonfname, "w")
        for key in nametags:
            old = nametags[key]
            new = repr(old)
            nametags[key] = new
            #print('nametags[%s] = %s' % (key, new))
        try:
            jsondumpsoutput = json.dumps(nametags, indent=4)
        except:
            print('json dumps failed on %s' % nametags)
            exit(1)
        #print('dumping %s' % str(jsondumpsoutput))
        jsonoutput.write(jsondumpsoutput)
        jsonoutput.write('\n')
        jsonoutput.close()

# Note this can be called directly also
def ParseValidateResultConfig(actual_parsing, homedir, studentlabdir, container_list, labidname, logger_in):
    MYHOME = homedir
    logger = logger_in
    configfilename = os.path.join(MYHOME,'.local','instr_config', 'results.config')
    configfile = open(configfilename)
    configfilelines = configfile.readlines()
    configfile.close()

    for line in configfilelines:
        linestrip = line.rstrip()
        if linestrip:
            if not linestrip.startswith('#'):
                #print "Current linestrip is (%s)" % linestrip
                try:
                    (each_key, each_value) = linestrip.split('=', 1)
                except:
                     logger.ERROR('missing "=" character in %s' % linestrip)
                     sys.exit(1)
                each_key = each_key.strip()
                ValidateConfigfile(actual_parsing, studentlabdir, container_list, labidname, each_key, each_value, logger)
                if each_key not in resultidlist:
                    resultidlist.append(each_key)
        #else:
        #    print "Skipping empty linestrip is (%s)" % linestrip

    return configfilelines, resultidlist

def ParseStdinStdout(homedir, studentlabdir, container_list, instructordir, labidname, logger_in):
    MYHOME = homedir
    logger = logger_in
    actual_parsing = True
    # Parse and Validate Results configuration file
    configfilelines, resultlist = ParseValidateResultConfig(actual_parsing, homedir, studentlabdir, container_list, labidname, logger_in)

    ''' process all results files (ignore name of function) for a student.  These
        are distrbuted amongst multiple containers, per container_list.
    '''
    jsonoutputfilename = labidname
    #print("ParseStdinStdout: jsonoutputfilename is (%s) studentlabdir %s" % (jsonoutputfilename, studentlabdir))
    logger.DEBUG("ParseStdinStdout: jsonoutputfilename is (%s) studentlabdir %s" % (jsonoutputfilename, studentlabdir))
  
    timestamplist.clear()

    del logfilelist[:]
    #del exec_proglist[:]
    del containernamelist[:]
    del stdinfnameslist[:]
    del stdoutfnameslist[:]

    #print "exec_proglist is: "
    #print exec_proglist
    #print "logfilelist is: "
    #print logfilelist
    OUTPUTRESULTHOME = '%s/%s' % (studentlabdir, ".local/result/")
    logger.DEBUG('Done with validate, outputresult to %s' % OUTPUTRESULTHOME)

    if not os.path.exists(OUTPUTRESULTHOME):
        os.makedirs(OUTPUTRESULTHOME)

    '''
    A round-about-way of getting all time stamps
    '''
    for mycontainername in container_list:
        RESULTHOME = '%s/%s/%s' % (studentlabdir, mycontainername, ".local/result/")
        logger.DEBUG('check results for %s' % RESULTHOME)
        if not os.path.exists(RESULTHOME):
            ''' expected, some containers don't have local results '''
            logger.DEBUG('result directory %s does not exist' % RESULTHOME)
            pass
            
        if mycontainername not in container_exec_proglist:
            logger.DEBUG('%s not in proglist %s' % (mycontainername, str(container_exec_proglist)))
            continue

        for exec_prog in container_exec_proglist[mycontainername]:
            stdinfiles = '%s%s.%s.' % (RESULTHOME, exec_prog, "stdin")
            stdoutfiles = '%s%s.%s.' % (RESULTHOME, exec_prog, "stdout")
            prgoutfiles = '%s%s.%s.' % (RESULTHOME, exec_prog, "prgout")
            logger.DEBUG('stdin %s stdout %s' % (stdinfiles, stdoutfiles))
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
            globprgoutfnames = glob.glob('%s*' % prgoutfiles)
            if globprgoutfnames != []:
                for prgoutfnames in globprgoutfnames:
                    stdoutfnameslist.append(prgoutfnames)

        for stdoutfname in stdoutfnameslist:
            # the only purpose of this is to establish the timestamp dictionary
            # only stdout is looked at.
            #print('for stdout %s' % stdoutfname)
            for exec_prog in container_exec_proglist[mycontainername]:
                stdoutfiles = '%s%s.%s.' % (RESULTHOME, exec_prog, "stdout")
                if stdoutfiles in stdoutfname:
                    #print "match"
                    (filenamepart, timestamppart) = stdoutfname.split(stdoutfiles)
                    targetmtime = os.path.getmtime(stdoutfname)
                    if timestamppart not in timestamplist:
                        #print('adding %s' % timestamppart)
                        timestamplist[timestamppart] = targetmtime
                    elif targetmtime > timestamplist[timestamppart]:
                        timestamplist[timestamppart] = targetmtime
                else:
                    #print "no match"
                    continue

    ''' process each timestamped result file. '''
    for timestamppart in timestamplist:
        targetmtime_string = datetime.datetime.fromtimestamp(timestamplist[timestamppart])
        end_time = targetmtime_string.strftime("%Y%m%d%H%M%S")
        outputjsonfname = '%s%s.%s' % (OUTPUTRESULTHOME, jsonoutputfilename, timestamppart)
        logger.DEBUG("ParseStdinStdout (1): Outputjsonfname is (%s)" % outputjsonfname)
        ParseConfigForFile(studentlabdir, labidname, configfilelines, outputjsonfname, 
                           container_list, timestamppart, end_time, logger)
    ''' process files without timestamps '''
    outputjsonfname = '%s%s' % (OUTPUTRESULTHOME, jsonoutputfilename)
    ParseConfigForFile(studentlabdir, labidname, configfilelines, outputjsonfname, container_list, None, None, logger)


