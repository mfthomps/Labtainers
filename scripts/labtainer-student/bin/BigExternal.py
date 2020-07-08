#!/usr/bin/env python3
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
import sys
import os
import shutil
def BigExternal(lab_dir, logger):
    '''
    Ensure large files named in the config/bigexternal.txt are present in the lab directory
    '''
    big_list = os.path.join(lab_dir,'config', 'bigexternal.txt')
    if not os.path.isfile(big_list):
        #print('Missing bigexternal.txt from %s' % big_list)
        return
    else:
        logger.debug('BigExternal file found: %s' % big_list)
    full = os.path.abspath(lab_dir)
    homedir = os.environ['HOME']
    cache_path = os.path.join(homedir, '.local', 'share', 'labtainer', 'big_cache')
    lab_cache = os.path.join(cache_path, os.path.basename(lab_dir))
    if os.path.isfile(big_list):
        with open(big_list) as fh:
            for line in fh:
               line = line.strip()
               if len(line) > 0 and not line.startswith('#'):
                   from_file, to_file = line.split()
                   to_path = os.path.join(lab_dir, to_file)
                   if not os.path.isfile(to_path):
                       cache_to_path = os.path.join(lab_cache, to_file)
                       try:
                           os.makedirs(os.path.dirname(cache_to_path))
                       except:
                           pass
                       if not os.path.isfile(cache_to_path):                       
                           logger.debug('missing %s, get it from %s success' % (to_path, from_file))
                           cmd = 'curl -L -R --create-dirs -o %s %s' % (to_path, from_file)
                           logger.debug('cmd: %s' % cmd)
                           ok = os.system(cmd)
                           logger.debug('result: %d' % ok)
                           shutil.copyfile(to_path, cache_to_path)
                       else:
                           try:
                               os.makedirs(os.path.dirname(to_path))
                           except:
                               pass
                           logger.debug('got %s from cache' % to_path)
                           shutil.copyfile(cache_to_path, to_path)
                   
                   else:
                       size = os.stat(to_path).st_size
                       if size < 50000:
                           if os.basename(to_path) == 'home.tar':
                               print('Remove the file at %s, and run again.' % to_path) 
                           else:
                               print('File at %s is supposed to be large.' % to_path)
                               print('Try removing the file and running again.  Or get the correct %s from %s' % (to_path, from_file))
                               exit(1) 
                    
