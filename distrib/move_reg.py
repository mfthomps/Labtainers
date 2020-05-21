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
import os
import sys
import argparse
sys.path.append('../scripts/labtainer-student/bin')
import InspectLocalReg
import InspectRemoteReg
import LabtainerLogging
'''
Move repos from the mfthomps registry to the labtainers registry
'''

def do_lab(lab_dir, lab, role, source_reg, dest_reg, force, logger):
    docker_dir = os.path.join(labdir, lab, 'dockerfiles')
    if not os.path.isdir(docker_dir):
        return
    df_list = [f for f in os.listdir(docker_dir) if os.path.isfile(os.path.join(docker_dir, f))]
    for df in df_list:
        if df.endswith('.swp'):
            continue
        try:
            parts = df.split('.')
            image = '%s.%s.%s' % (parts[1], parts[2], role)
        except:
            print('could not get image from %s' % df);
            continue
        with_new_reg = '%s/%s' % (dest_reg, image)
        new_created, new_user, version, tag = InspectRemoteReg.inspectRemote(with_new_reg, logger, no_pull=True)
        if new_created is not None:
            with_reg = '%s/%s' % (source_reg, image)
            remote_created, remote_user, version, tag = InspectRemoteReg.inspectRemote(with_reg, logger, no_pull=True)
        if force or new_created is None or remote_created > new_created:
            cmd = 'docker pull %s/%s' % (source_reg, image)
            print(cmd)
            os.system(cmd)
            cmd = 'docker tag %s/%s %s/%s' % (source_reg, image, dest_reg, image)
            print(cmd)
            os.system(cmd)
            cmd = 'docker push %s/%s' % (dest_reg, image)
            print(cmd)
            os.system(cmd)
        else:
            print('local registry for %s is up to date.' % image)

parser = argparse.ArgumentParser(description='pull from the docker hub mfthomps and push to docker hub labtainers')
parser.add_argument('-l', '--lab', action='store', help='only pull/tag/push this lab')
parser.add_argument('-f', '--force', action='store_true', default=False, help='force pull/push')
args = parser.parse_args()
skip = []
with open('skip-labs') as fh:
   for line in fh:
       f = os.path.basename(line).strip()
       print('will skip [%s]' % f)
       skip.append(f)

logger = LabtainerLogging.LabtainerLogging("reg_image_dif.log", 'none', "../config/labtainer.config")
labdir = '../labs'
lab_list = os.listdir(labdir)
#
# test with a single lab.  Then use loop below once it works.
#
new_registry = 'labtainers'
os.system('docker login -u mfthomps')
if args.lab is not None:
    do_lab(labdir, args.lab, 'student', 'mfthomps', new_registry, args.force, logger)
else:
    #print('commented out for now')
    for lab in sorted(lab_list):
        if lab not in skip:
            start_config = os.path.join('../labs', lab, 'config', 'start.config')
            cmd = 'git ls-files --error-unmatch %s > /dev/null 2>&1' % start_config
            result = os.system(cmd)
            if result == 0:
                do_lab(labdir, lab, 'student', 'mfthomps', new_registry, args.force, logger)
