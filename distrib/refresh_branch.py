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
import argparse
import subprocess
sys.path.append('../scripts/labtainer-student/bin')
import LocalBase
import InspectLocalReg
import LabtainerLogging
import ParseLabtainerConfig
import registry

'''
Force the registry associated with the current git branch (see config/registry.config)
to match the premaster registry.  Intended to be called from scripts, e.g., to establish
a new branch.  Not intended to be invoked directly.
'''
def pull_push(image, source_registry, dest_registry):
    with_registry = '%s/%s' % (source_registry, image)
    cmd = 'docker pull %s' % with_registry
    print(cmd)
    os.system(cmd)
    cmd = 'docker tag %s/%s %s/%s' % (source_registry, image, dest_registry, image)
    print(cmd)
    os.system(cmd)
    cmd = 'docker push %s/%s' % (dest_registry, image)
    print(cmd)
    os.system(cmd)

def do_lab(lab_dir, lab, role, source_reg, dest_reg, logger, no_copy):
    ''' use dockerfiles to determine the set of containers '''
    print('Lab: %s' % lab)
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
            container = parts[2]
        except:
            print('could not get image from %s' % df);
            continue
        dest_created, dest_user, dest_version, tag, base  = InspectLocalReg.inspectLocal(image, logger, dest_reg, no_pull=True)

        if dest_created is not None:
            with_reg = '%s/%s' % (source_reg, image)
            source_created, source_user, dest_version, tag, base  = InspectLocalReg.inspectLocal(image, logger, source_reg, no_pull=True)
            if source_created != dest_created:
                print('DIFFERENT: %s:%s source created/version %s/%s  destination: %s/%s' % (lab, container, source_created, 
                      source_version, dest_created, dest_version))
                pull_push(image, source_reg, dest_reg)
        else:
            pull_push(image, source_reg, dest_reg)

def doBases(source_registry, dest_registry):
    base_names = ['base', 'network', 'firefox', 'wireshark', 'java', 'centos', 'centos.xtra', 'lamp', 'lamp.xtra', 'kali', 'metasploitable']
    print('Comparing base images in %s to  %s, and replacing content of %s if different' % (dest_registry, source_registry, dest_registry))
    for base in base_names:
        full = 'labtainer.%s' % (base)
        with_registry = '%s/labtainer.%s' % (source_registry, base)
        print(full)
        source_created, local_user = LocalBase.inspectLocal(full, lgr, source_registry)
        dest_created, local_user = LocalBase.inspectLocal(full, lgr, dest_registry)
        if source_created != dest_created:
            print('Difference in %s,  source: %s  destination: %s' % (full, source_created, dest_created))
            if not args.no_copy:
                pull_push(full, source_registry, dest_registry)

parser = argparse.ArgumentParser(description='Compare a source registry with a destination registry, and update the destination so they match')
parser.add_argument('-n', '--no_copy', action='store_true', default=False, help='Do not modify registry, just report differences')
parser.add_argument('-l', '--lab', action='store', help='only check this lab')
args = parser.parse_args()

config_file = '../config/labtainer.config'
labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(config_file, None)
lgr = LabtainerLogging.LabtainerLogging("refresh_branch.log", 'none', config_file)

''' source is always the mirror '''
source_registry = labtainer_config.test_registry
branch, dest_registry = registry.getBranchRegistry()
if dest_registry is None:
    print('No registry found for branch %s' % branch)
    exit(1)

labdir = '../labs'
if args.lab is not None:
    do_lab(labdir, args.lab, 'student', source_registry, dest_registry, lgr, args.no_copy)
else:
    grader = 'labtainer.grader'
    pull_push(grader, source_registry, dest_registry)
    
    doBases(source_registry, dest_registry)
    skip = []
    with open('skip-labs') as fh:
       for line in fh:
           f = os.path.basename(line).strip()
           print('will skip [%s]' % f)
           skip.append(f)

    mycwd = os.getcwd()
    os.chdir(labdir)
    cmd = 'git ls-files ./ | cut -d/ -f1 | uniq'
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = child.communicate()
    lab_list = output[0].decode('utf-8').strip().splitlines(True)
    os.chdir(mycwd)
    for lab in sorted(lab_list):
        lab = lab.strip()
        if lab not in skip:
            do_lab(labdir, lab, 'student', source_registry, dest_registry, lgr, args.no_copy)

