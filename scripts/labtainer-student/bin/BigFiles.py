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
def BigFiles(lab_dir):
    '''
    Ensure large files named in the config/bigfiles.txt are present in the lab directory
    '''
    big_list = os.path.join(lab_dir,'config', 'bigfiles.txt')
    if not os.path.isfile(big_list):
        #print('Missing bigfiles.txt from %s' % big_list)
        return
    full = os.path.abspath(lab_dir)
    top = full[:full.index('labs')]
    if os.path.isfile(big_list):
        with open(big_list) as fh:
            for line in fh:
               line = line.strip()
               if len(line) > 0 and not line.startswith('#'):
                   from_file, to_file = line.split()
                   from_path = os.path.join(top,'bigfiles', from_file)
                   to_path = os.path.join(lab_dir, to_file)
                   if not os.path.isfile(to_path):
                       if not os.path.isfile(from_path):
                           print('Missing large file: %s' % from_path)
                           print('Get it from https://nps.box.com/v/LabtainersBigFiles' % from_file)
                           exit(1)
                       else:
                           try:
                               os.makedirs(os.path.dirname(to_path))
                           except:
                               pass
                           shutil.copy2(from_path, to_path)
                    
if __name__ == '__main__':               
    lab_dir = sys.argv[1]
    BigFiles(lab_dir)
