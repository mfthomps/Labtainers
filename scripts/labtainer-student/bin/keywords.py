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
import labList
''' Read keywords from each lab and print a list of them '''
def list():
    labtainer_dir = os.getenv('LABTAINER_DIR') 
    if labtainer_dir is None:
        print('LABTAINER_DIR not defined')
        exit(1)
    labs_dir = os.path.join(labtainer_dir, 'labs')
    #lablist = os.listdir(labs_dir) 
    lablist = labList.getLabs()
    key_list = []
    for lab in lablist:
        keypath = os.path.join(labs_dir, lab, 'config', 'keywords.txt')
        if os.path.isfile(keypath):
            with open(keypath) as fh:
                for line in fh:
                    key = line.strip()
                    if key not in key_list and len(key)>0:
                        key_list.append(key)

    for key in sorted(key_list):
        print(key)
  
''' Find labs having the given keyword ''' 
def find(keyword):
    labtainer_dir = os.getenv('LABTAINER_DIR') 
    if labtainer_dir is None:
        print('LABTAINER_DIR not defined')
        exit(1)
    labs_dir = os.path.join(labtainer_dir, 'labs')
    #labdirs = os.listdir(labs_dir) 
    labdirs = labList.getLabs()
    lab_list = []
    lab_descrip = []
    for lab in labdirs:
        keypath = os.path.join(labs_dir, lab, 'config', 'keywords.txt')
        if os.path.isfile(keypath):
            with open(keypath) as fh:
                for line in fh:
                    if len(line.strip()) == 0:
                        continue
                    if keyword.startswith(line.strip()) or line.startswith(keyword):
                        if lab not in lab_list: 
                            lab_list.append(lab)
                            about_path = os.path.join(labs_dir, lab, 'config', 'about.txt')
                            if os.path.isfile(about_path):
                                with open(about_path) as about_fh:
                                    descrip = '%s -- %s' % (lab, about_fh.read())
                                    lab_descrip.append(descrip)
                            else:
                                lab_descrip.append(lab)
    for lab in sorted(lab_descrip):
        print(lab)
