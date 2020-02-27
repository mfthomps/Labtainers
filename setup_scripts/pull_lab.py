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
sys.path.append('../scripts/labtainer-student/bin')
import LabtainerLogging
import ParseLabtainerConfig
import registry

'''
pull a lab's images
'''

def doLab(lab_dir, lab, reg, logger):
    ''' use dockerfiles to determine the set of containers '''
    print('Lab: %s' % (lab))
    docker_dir = os.path.join(lab_dir, lab, 'dockerfiles')
    if not os.path.isdir(docker_dir):
        return
    df_list = [f for f in os.listdir(docker_dir) if os.path.isfile(os.path.join(docker_dir, f))]
    for df in df_list:
        if df.endswith('.swp'):
            continue
        try:
            parts = df.split('.')
            image = '%s.%s.student' % (parts[1], parts[2])
            container = parts[2]
        except:
            print('could not get image from %s' % df);
            continue
        cmd = 'docker pull %s/%s' % (reg, image)
        print('cmd: %s' % cmd)
        os.system(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pull the images for a given lab. Intended to prep a VM for use with no Internet')
    parser.add_argument('labname', action='store', help='The lab to pull')
    args = parser.parse_args()

    config_file = os.path.join(os.getenv('LABTAINER_DIR'), 'config', 'labtainer.config')
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(config_file, None)
    lgr = LabtainerLogging.LabtainerLogging("/tmp/pull.log", 'none', config_file)
   
    branch, registry = registry.getBranchRegistry()

    if registry is None:
        print('No registry found for branch %s' % branch)
        exit(1)
    labdir = os.path.join(os.getenv('LABTAINER_DIR'), 'labs')
    doLab(labdir, args.labname, registry, lgr)

