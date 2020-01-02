'''
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''
import os
import datetime
import json
'''
Keep a count of lab starts and redos.
'''
def getPath(start_path, labname):
    count_path = os.path.join(start_path, '.tmp', labname, 'count.json')
    if not os.path.isdir(os.path.dirname(count_path)):
       os.makedirs(os.path.dirname(count_path)) 
    return count_path

def addCount(start_path, labname, is_redo, logger):
    current_time_string = str(datetime.datetime.now())
    current_count = getLabCount(start_path, labname, logger)
    writeLabCount(start_path, labname, is_redo, current_count, current_time_string, logger)
    return len(current_count['start']+current_count['redo'])

def getLabCount(start_path, labname, logger):
    current_count = {}
    count_path = getPath(start_path, labname)
    if os.path.isfile(count_path):
        with open(count_path) as f:
            try:
                current_count = json.load(f)
            except:
                logger.debug('json load failed on %s, reset the counts.' % count_path)
                current_count['start'] = []
                current_count['redo'] = []
    else:
        current_count['start'] = []
        current_count['redo'] = []

    return current_count

def writeLabCount(start_path, labname, is_redo, current_count, current_time_string, logger):
    if is_redo:
        current_count['redo'].append(current_time_string)
    else:
        if 'normal' in current_count:
            current_count['normal'].append(current_time_string)
        else:
            try:
                current_count['start'].append(current_time_string)
            except:
                return
     
    count_path = getPath(start_path, labname)
    labname_file = open(count_path, "w")
    try:
        jsondumpsoutput = json.dumps(current_count, indent=4)
    except:
        logger.debug('json dumps failed on %s' % current_count)
        exit(1)
    labname_file.write(jsondumpsoutput)
    labname_file.write('\n')
    labname_file.close()
