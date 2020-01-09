#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
sys.path.append('../scripts/labtainer-student/bin')
import LocalBase
import InspectLocalReg
import LabtainerLogging
import ParseLabtainerConfig

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

def getBranchRegistry():
    cmd = 'git rev-parse --abbrev-ref HEAD'
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    branch = None
    registry = None
    if len(output[0].strip()) > 0:
        branch = output[0].decode('utf-8').strip()
        registry_file = '../config/registry.config'
        if os.path.isfile(registry_file):
            with open(registry_file) as fh:
                for line in fh:
                    parts = line.split()
                    if parts[0] == branch: 
                        registry = 'testregistry:%s' % parts[1]
                        break
        else:
            print('No config/registry.config file')
            exit(1)
    else:
        print('No branch found')
        exit(1)
        
    return branch, registry

parser = argparse.ArgumentParser(description='Compare a source registry with a destination registry, and update the destination so they match')
parser.add_argument('-n', '--no_copy', action='store_true', default=False, help='Do not modify registry, just report differences')
parser.add_argument('-l', '--lab', action='store', help='only check this lab')
args = parser.parse_args()

config_file = '../config/labtainer.config'
labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(config_file, None)
lgr = LabtainerLogging.LabtainerLogging("refresh_branch.log", 'none', config_file)

''' source is always the mirror '''
source_registry = labtainer_config.test_registry
branch, dest_registry = getBranchRegistry()
if dest_registry is None:
    print('No registry found for branch %s' % branch)
    exit(1)

labdir = '../labs'
if args.lab is not None:
    do_lab(labdir, args.lab, 'student', source_registry, dest_registry, lgr, args.no_copy)
else:
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

