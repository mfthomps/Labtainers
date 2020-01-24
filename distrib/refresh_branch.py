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
import LabtainerBase

'''
Force the registry associated with the current git branch (see config/registry.config)
to match the premaster registry.  Intended to be called from scripts, e.g., to establish
a new branch.
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

def checkDates(image, source_reg, dest_reg, no_copy, lab, logger):
        dest_created, dest_user, dest_version, tag, base  = InspectLocalReg.inspectLocal(image, logger, dest_reg, no_pull=True)

        if dest_created is not None:
            with_reg = '%s/%s' % (source_reg, image)
            source_created, source_user, source_version, tag, base  = InspectLocalReg.inspectLocal(image, logger, source_reg, no_pull=True)
            if source_created != dest_created:
                print('DIFFERENT: %s:%s source created/version %s/%s  destination: %s/%s' % (lab, image, source_created, 
                      source_version, dest_created, dest_version))
                logger.debug('DIFFERENT: %s:%s source created/version %s/%s  destination: %s/%s' % (lab, image, source_created, 
                      source_version, dest_created, dest_version))
                if not no_copy:
                    pull_push(image, source_reg, dest_reg)
        else:
            print('%s not in %s, would add it' % (image, dest_reg))
            if not no_copy:
                pull_push(image, source_reg, dest_reg)

def doLab(lab_dir, lab, role, source_reg, dest_reg, logger, no_copy):
    ''' use dockerfiles to determine the set of containers '''
    print('Lab: %s No_copy %r' % (lab, no_copy))
    docker_dir = os.path.join(lab_dir, lab, 'dockerfiles')
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
        checkDates(image, source_reg, dest_reg, no_copy, lab, logger)

def doBases(source_registry, dest_registry, no_copy):
    print('Comparing base images in %s to  %s, and replacing content of %s if different' % (dest_registry, source_registry, dest_registry))
    base_names = LabtainerBase.getBaseList()
    for base in base_names:
        with_registry = '%s/%s' % (source_registry, base)
        print(base)
        source_created, local_user = LocalBase.inspectLocal(base, lgr, source_registry)
        dest_created, local_user = LocalBase.inspectLocal(base, lgr, dest_registry)
        if source_created != dest_created:
            print('Difference in %s,  source: %s  destination: %s' % (base, source_created, dest_created))
            if not no_copy:
                pull_push(base, source_registry, dest_registry)


def updateRegistry(source_registry, dest_registry, lgr, lab, no_copy, quiet=False):
    
    labdir = os.path.join(os.getenv('LABTAINER_DIR'), 'labs')
    if lab is not None:
        doLab(labdir, lab, 'student', source_registry, dest_registry, lgr, no_copy)
    else:
        if not quiet:
            msg = 'Will modify registry %s to match %s.  Continue? (y/n)' % (dest_registry, source_registry)
            response = input(msg)
            if response.lower() != 'y':
                print('Exiting')
                exit(0)
        grader = 'labtainer.grader'
        checkDates(grader, source_registry, dest_registry, no_copy, 'grader', lgr)
        
        doBases(source_registry, dest_registry, no_copy)
        skip = []
        with open('skip-labs') as fh:
           for line in fh:
               f = os.path.basename(line).strip()
               #print('will skip [%s]' % f)
               skip.append(f)
    
        mycwd = os.getcwd()
        os.chdir(labdir)
        cmd = 'git ls-files ./ | cut -d/ -f1 | uniq'
        child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = child.communicate()
        lab_list = output[0].decode('utf-8').strip().splitlines()
        os.chdir(mycwd)
        for lab in sorted(lab_list):
            lab = lab.strip()
            if lab not in skip:
                doLab(labdir, lab, 'student', source_registry, dest_registry, lgr, no_copy)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare a source registry with a destination registry, and update the destination so they match')
    parser.add_argument('-n', '--no_copy', action='store_true', default=False, help='Do not modify registry, just report differences')
    parser.add_argument('-l', '--lab', action='store', help='only check this lab')
    parser.add_argument('-q', '--quiet', action='store_true', default=False,  help='Do not prompt for confirmation.')
    args = parser.parse_args()

    config_file = os.path.join(os.getenv('LABTAINER_DIR'), 'config', 'labtainer.config')
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(config_file, None)
    lgr = LabtainerLogging.LabtainerLogging("refresh_branch.log", 'none', config_file)
   
    ''' source is the premaster mirror '''
    source_registry = labtainer_config.test_registry
    branch, dest_registry = registry.getBranchRegistry()

    if dest_registry is None:
        print('No registry found for branch %s' % branch)
        exit(1)
    updateRegistry(source_registry, dest_registry, lgr, args.lab, args.no_copy, args.quiet)

