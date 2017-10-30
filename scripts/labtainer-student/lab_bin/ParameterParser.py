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

# ParameterParser.py
# Description: * Read parameter.config
#              * Parse stdin and stdout files based on parameter.config
#              * Create a json file

import json
import glob
import md5
import os
import random
import sys
import ParameterizeLogging

watermarkcreatelist = {}
randreplacelist = {}
hashcreatelist = {}
hashreplacelist = {}
paramlist = {}
global container_name

logger = ParameterizeLogging.ParameterizeLogging("/tmp/parameterize.log")

def WatermarkCreate(container_user, lab_instance_seed, logger):
    the_watermark_string = "LABTAINER_WATERMARK1"
    # Create hash per the_watermark_string (note: there is only one watermark file for now)
    string_to_be_hashed = '%s:%s' % (lab_instance_seed, the_watermark_string)
    mymd5 = md5.new()
    mymd5.update(string_to_be_hashed)
    mymd5_hex_string = mymd5.hexdigest()
    #logger.DEBUG(mymd5_hex_string)

    # Assume only one watermark file with filename /home/<container_user>/.local/.watermark
    myfilename = '/home/%s/.local/.watermark' % container_user

    # If file does not exist, create an empty file
    if not os.path.exists(myfilename):
        outfile = open(myfilename, 'w')
        outfile.write('')
        outfile.close()

    # Only one watermark file for now
    watermarkcreatelist[myfilename] = []
    watermarkcreatelist[myfilename].append('%s' % mymd5_hex_string)

    #logger.DEBUG("Perform_WATERMARK_CREATE")
    for (listfilename, createlist) in watermarkcreatelist.items():
        filename = listfilename
        #logger.DEBUG("Current Filename is %s" % filename)
        #print "Watermark Create list is "
        #print createlist
        # open the file - write
        outfile = open(filename, 'w')
        for the_string in createlist:
            outfile.write('%s\n' % the_string)
        outfile.close()

def CheckRandReplaceEntry(container_user, lab_instance_seed, param_id, each_value, logger):
    # RAND_REPLACE : <filename> : <token> : <LowerBound> : <UpperBound>
    #print "Checking RAND_REPLACE entry"
    entryline = each_value.split(': ')
    #print entryline
    numentry = len(entryline)
    if numentry != 4:
        logger.ERROR("RAND_REPLACE (%s) improper format" % each_value)
        #logger.ERROR("RAND_REPLACE : <filename> : <token> : <LowerBound> : <UpperBound>")
        sys.exit(1)
    myfilename_field = entryline[0].strip()
    token = entryline[1].strip()
    #print "filename is (%s)" % myfilename
    #print "token is (%s)" % token

    # Converts lowerbound and upperbound as integer - and pass to
    # random.randint(a,b)
    # Starts with assuming will use integer (instead of hexadecimal)
    use_integer = True
    lowerboundstr = entryline[2].strip()
    if lowerboundstr.startswith('0x'):
        use_integer = False
        lowerbound_int = int(lowerboundstr, 16)
    else:
        lowerbound_int = int(lowerboundstr, 10)
    upperboundstr = entryline[3].strip()
    if upperboundstr.startswith('0x'):
        if use_integer == True:
            # Inconsistent format of lowerbound (integer format)
            # vs upperbound (hexadecimal format)
            logger.ERROR("RAND_REPLACE (%s) inconsistent lowerbound/upperbound format" % each_value)
            #logger.ERROR("RAND_REPLACE : <filename> : <token> : <LowerBound> : <UpperBound>")
            sys.exit(1)
        use_integer = False
        upperbound_int = int(upperboundstr, 16)
    else:
        if use_integer == False:
            # Inconsistent format of lowerbound (hexadecimal format)
            # vs upperbound (integer format)
            logger.ERROR("RAND_REPLACE (%s) inconsistent lowerbound/upperbound format" % each_value)
            #logger.ERROR("RAND_REPLACE : <filename> : <token> : <LowerBound> : <UpperBound>")
            sys.exit(1)
        upperbound_int = int(upperboundstr, 10)
    #print "lowerbound is (%d)" % lowerbound_int
    #print "upperbound is (%d)" % upperbound_int
    if lowerbound_int > upperbound_int:
        logger.ERROR("RAND_REPLACE (%s) lowerbound greater than upperbound" % each_value)
        sys.exit(1)
    random_int = random.randint(lowerbound_int, upperbound_int)
    #print "random value is (%d)" % random_int
    if use_integer:
        random_str = '%s' % int(random_int)
    else:
        random_str = '%s' % hex(random_int)

    myfilename_list = myfilename_field.split(';')
    for myfilename in myfilename_list:
        # Check to see if ':' in myfilename
        if ':' in myfilename:
            # myfilename has the container_name also
            tempcontainer_name, myactualfilename = myfilename.split(':')
            # Assume filename is relative to /home/<container_user>
            if not myactualfilename.startswith('/'):
                user_home_dir = '/home/%s' % container_user
                myfullactualfilename = os.path.join(user_home_dir, myactualfilename)
            else:
                myfullactualfilename = myactualfilename
            myfilename = '%s:%s' % (tempcontainer_name, myfullactualfilename)
        else:
            # myfilename does not have the containername
            # Assume filename is relative to /home/<container_user>
            if not myfilename.startswith('/'):
                user_home_dir = '/home/%s' % container_user
                myfullfilename = os.path.join(user_home_dir, myfilename)
            else:
                myfullfilename = myfilename
            myfilename = myfullfilename
    
        if myfilename in randreplacelist:
            randreplacelist[myfilename].append('%s:%s' % (token, random_str))
        else:
            randreplacelist[myfilename] = []
            randreplacelist[myfilename].append('%s:%s' % (token, random_str))
    paramlist[param_id] = random_str


def CheckHashCreateEntry(container_user, lab_instance_seed, param_id, each_value, logger):
    # HASH_CREATE : <filename> : <string>
    #print "Checking HASH_CREATE entry"
    entryline = each_value.split(': ')
    #print entryline
    numentry = len(entryline)
    if numentry != 2 and numentry != 3:
        logger.ERROR("HASH_CREATE : <filename> : <string> [: length]")
        sys.exit(1)
    myfilename_field = entryline[0].strip()
    the_string = entryline[1].strip()
    strlen = 32
    if numentry == 3:
        try:
            strlen = int(entryline[2].strip())
        except:      
            logger.ERROR("HASH_CREATE (%s) improper format" % each_value)
            logger.ERROR("expected int for length, got %s" % entryline[2])
            sys.exit(1)

    # Create hash per the_string
    string_to_be_hashed = '%s:%s' % (lab_instance_seed, the_string)
    mymd5 = md5.new()
    mymd5.update(string_to_be_hashed)
    mymd5_hex_string = mymd5.hexdigest()[:strlen]
    #print mymd5_hex_string
    #print "filename is (%s)" % myfilename_field
    #print "the_string is (%s)" % the_string
    #print "mymd5_hex_string is (%s)" % mymd5_hex_string
    # If container_user == "" then it must be instructor container
    # then skip actual creation of hash file
    if container_user != "":
        # Check to see if ':' in myfilename
        myfilename_list = myfilename_field.split(';')
        for myfilename in myfilename_list:
            if ':' in myfilename:
                # myfilename has the container_name also
                tempcontainer_name, myactualfilename = myfilename.split(':')
                # Assume filename is relative to /home/<container_user>
                if not myactualfilename.startswith('/'):
                    user_home_dir = '/home/%s' % container_user
                    myfullactualfilename = os.path.join(user_home_dir, myactualfilename)
                else:
                    myfullactualfilename = myactualfilename
                myfilename = '%s:%s' % (tempcontainer_name, myfullactualfilename)
            else:
                # myfilename does not have the containername
                # Assume filename is relative to /home/<container_user>
                if not myfilename.startswith('/'):
                    user_home_dir = '/home/%s' % container_user
                    myfullfilename = os.path.join(user_home_dir, myfilename)
                else:
                    myfullfilename = myfilename
                myfilename = myfullfilename

            # If file does not exist, create an empty file
            if not os.path.exists(myfilename):
                outfile = open(myfilename, 'w')
                outfile.write('')
                outfile.close()

            if myfilename in hashcreatelist:
                hashcreatelist[myfilename].append('%s' % mymd5_hex_string)
            else:
                hashcreatelist[myfilename] = []
                hashcreatelist[myfilename].append('%s' % mymd5_hex_string)

    # Update paramlist regardless
    paramlist[param_id] = mymd5_hex_string

def CheckHashReplaceEntry(container_user, lab_instance_seed, param_id, each_value, logger):
    # HASH_REPLACE : <filename> : <token> : <string>
    #print "Checking HASH_REPLACE entry"
    entryline = each_value.split(': ')
    #print entryline
    numentry = len(entryline)
    if numentry != 3 and numentry != 4:
        logger.ERROR("HASH_REPLACE (%s) improper format" % each_value)
        #logger.ERROR("HASH_REPLACE : <filename> : <symbol> : <string> [: length]")
        sys.exit(1)
    strlen = 32
    if numentry == 4:
        try:
            strlen = int(entryline[3].strip())
        except:      
            logger.ERROR("HASH_REPLACE (%s) improper format" % each_value)
            logger.ERROR("expected int for length, got %s" % entryline[3])
            sys.exit(1)
    myfilename_field = entryline[0].strip()
    token = entryline[1].strip()
    the_string = entryline[2].strip()
    # Create hash per the_string
    string_to_be_hashed = '%s:%s' % (lab_instance_seed, the_string)
    mymd5 = md5.new()
    mymd5.update(string_to_be_hashed)
    mymd5_hex_string = mymd5.hexdigest()[:strlen]
    #print "filename is (%s)" % myfilename_field
    #print "token is (%s)" % token
    #print "the_string is (%s)" % the_string

    # Check to see if ':' in myfilenamb
    myfilename_list = myfilename_field.split(';')
    for myfilename in myfilename_list:
        if ':' in myfilename:
            # myfilename has the container_name also
            tempcontainer_name, myactualfilename = myfilename.split(':')
            # Assume filename is relative to /home/<container_user>
            if not myactualfilename.startswith('/'):
                user_home_dir = '/home/%s' % container_user
                myfullactualfilename = os.path.join(user_home_dir, myactualfilename)
            else:
                myfullactualfilename = myactualfilename
            myfilename = '%s:%s' % (tempcontainer_name, myfullactualfilename)
        else:
            # myfilename does not have the containername
            # Assume filename is relative to /home/<container_user>
            if not myfilename.startswith('/'):

                user_home_dir = '/home/%s' % container_user
                myfullfilename = os.path.join(user_home_dir, myfilename)
            else:
                myfullfilename = myfilename
            myfilename = myfullfilename

        if myfilename in hashreplacelist:
            hashreplacelist[myfilename].append('%s:%s' % (token, mymd5_hex_string))
        else:
            hashreplacelist[myfilename] = []
            hashreplacelist[myfilename].append('%s:%s' % (token, mymd5_hex_string))
    paramlist[param_id] = mymd5_hex_string


def ValidateParameterConfig(container_user, lab_instance_seed, param_id, each_key, each_value, logger):
    if each_key == "RAND_REPLACE":
        #print "RAND_REPLACE"
        CheckRandReplaceEntry(container_user, lab_instance_seed, param_id, each_value, logger)
    elif each_key == "HASH_CREATE":
        #print "HASH_CREATE"
        CheckHashCreateEntry(container_user, lab_instance_seed, param_id, each_value, logger)
    elif each_key == "HASH_REPLACE":
        #print "HASH_REPLACE"
        CheckHashReplaceEntry(container_user, lab_instance_seed, param_id, each_value, logger)
    else:
        logger.ERROR("ParseParameter.py, ValidateParameterConfig, Invalid operator %s" % each_key)
        sys.exit(1)
    return 0

# Perform RAND_REPLACE
def Perform_RAND_REPLACE(lab_instance_seed, logger):
    global container_name
    # At this point randreplacelist should have been populated
    # and files have been confirmed to exist

    #print "Perform_RAND_REPLACE"
    for (listfilename, replacelist) in randreplacelist.items():
        # Check to see if ':' in myfilename
        if ':' in listfilename:
            # listfilename has the containername also
            if container_name != "" and listfilename.startswith(container_name):
                tmp_container_name, filename = listfilename.split(':')
            else:
                # Not for this container
                continue
        else:
            filename = listfilename
        #print "Current Filename is %s" % filename
        if not os.path.exists(filename):
            logger.ERROR("Perform_RAND_REPLACE: File %s does not exist" % filename)
            sys.exit(1)
        #else:
        #    print "File (%s) exist\n" % filename
        #print "Replace list is "
        #print replacelist
        content = None
        # First open the file - read
        with open(filename, 'r') as infile:
            content = infile.read()
            for replaceitem in replacelist:
                (oldtoken, newtoken) = replaceitem.split(':')
                content = content.replace(oldtoken, newtoken)
        # Re-open file with write
        with open(filename, 'w') as outfile:
            outfile.write(content)
        

# Perform HASH_CREATE
def Perform_HASH_CREATE(lab_instance_seed, logger):
    global container_name
    # At this point hashcreatelist should have been populated
    # and files have been confirmed to exist or created

    #print "Perform_HASH_CREATE"
    for (listfilename, createlist) in hashcreatelist.items():
        # Check to see if ':' in myfilename
        if ':' in listfilename:
            # listfilename has the containername also
            if container_name != "" and listfilename.startswith(container_name):
                container_name, filename = listfilename.split(':')
            else:
                # Not for this container
                continue
        else:
            filename = listfilename
        #print "Current Filename is %s" % filename
        #print "Hash Create list is "
        #print createlist
        # open the file - write
        outfile = open(filename, 'w')
        for the_string in createlist:
            outfile.write('%s\n' % the_string)
        outfile.close()

# Perform HASH_REPLACE
def Perform_HASH_REPLACE(lab_instance_seed, logger):
    global container_name
    # At this point hashreplacelist should have been populated
    # and files have been confirmed to exist

    #print "Perform_HASH_REPLACE"
    #print hashreplacelist
    for (listfilename, replacelist) in hashreplacelist.items():
        # Check to see if ':' in myfilename
        if ':' in listfilename:
            # listfilename has the containername also
            #print "listfilename is (%s)" % listfilename
            #print "container_name is (%s)" % container_name
            if container_name != "" and listfilename.startswith(container_name):
                #print "Yes it startswith"
                container_name, filename = listfilename.split(':')
            else:
                #print "No it does not startswith"
                # Not for this container
                continue
        else:
            #print "Does not have :"
            filename = listfilename
        #print "Current Filename is %s" % filename
        if not os.path.exists(filename):
            logger.ERROR("Perform_HASH_REPLACE: File %s does not exist" % filename)
            sys.exit(1)
        #else:
        #    print "File (%s) exist\n" % filename
        #print "Replace list is "
        #print replacelist
        content = None
   
        with open(filename, 'r') as infile:
            content = infile.read() 
            for replaceitem in replacelist:
                (oldtoken, newtoken) = replaceitem.split(':')
                content = content.replace(oldtoken, newtoken)
        # Re-open file with write
        with open(filename, 'w') as outfile:
            outfile.write(content)

def DoReplace(container_user, lab_instance_seed, logger):
    # Do create Watermark here - instructor container does not call this
    #print "WATERMARK_CREATE"
    WatermarkCreate(container_user, lab_instance_seed, logger)

    # Perform RAND_REPLACE
    Perform_RAND_REPLACE(lab_instance_seed, logger)
    # Perform HASH_CREATE
    Perform_HASH_CREATE(lab_instance_seed, logger)
    # Perform HASH_REPLACE
    Perform_HASH_REPLACE(lab_instance_seed, logger)

def ParseParameterConfig(container_user, lab_instance_seed, configfilename, logger_in):
    logger = logger_in
    # Seed random with lab seed
    random.seed(lab_instance_seed)
    configfile = open(configfilename)
    configfilelines = configfile.readlines()
    configfile.close()
  
    for line in configfilelines:
        linestrip = line.rstrip()
        if linestrip:
            if not linestrip.startswith('#'):
                #print "Current linestrip is (%s)" % linestrip
                (param_id, each_key, each_value) = linestrip.split(': ', 2)
                each_key = each_key.strip()
                param_id = param_id.strip()
                ValidateParameterConfig(container_user, lab_instance_seed, param_id, each_key, each_value, logger)
        #else:
        #    print "Skipping empty linestrip is (%s)" % linestrip
    return paramlist



# Usage: ParameterParser.py <lab_instance_seed> <container_name> [<config_file>]
# Arguments:
#     <container_user> - username of the container
#     <lab_instance_seed> - laboratory instance seed
#     <container_name> - name of the container"
#     [<config_file>] - optional configuration file
#                       if <config_file> not specified, it defaults to
def main():
    global container_name
    #print "Running ParameterParser.py"
    numargs = len(sys.argv)
    if not (numargs == 4 or numargs == 5):
        logger.ERROR("ParameterParser.py <container_user> <lab_instance_seed> <container_name> [<config_file>]")
        sys.exit(1)

    container_user = sys.argv[1]
    lab_instance_seed = sys.argv[2]
    try:
        container_name = sys.argv[3].split('.')[1]
    except:
        logger.ERROR('Could not parse container name from %s' % sys.argv[3])
        sys.exit(1)
        
    if numargs == 5:
        configfilename = sys.argv[4]
    else:
        configfilename = '/home/%s/.local/config/%s' % (container_user, "parameter.config")

    ParseParameterConfig(container_user, lab_instance_seed, configfilename, logger)
    DoReplace(container_user, lab_instance_seed, logger)
    return 0

if __name__ == '__main__':
    sys.exit(main())

