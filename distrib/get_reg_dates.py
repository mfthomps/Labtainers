#!/usr/bin/python3
import argparse
import os
import sys
import subprocess
sys.path.append('../scripts/labtainer-student/bin')
import LabtainerLogging
import labutils
import registry
import InspectLocalReg
import ParseLabtainerConfig
import InspectRemoteReg

def getDates(image, reg, lab, logger):
        if reg == 'mfthomps':
            with_reg = '%s/%s' % (reg, image)
            created, user, version, tag = InspectRemoteReg.inspectRemote(with_reg, logger, no_pull=True)
        else:
            created, user, version, tag, base  = InspectLocalReg.inspectLocal(image, logger, reg, no_pull=True)

        if created is not None:
            print('%s %s %s' % (lab, image, created))

def doLab(lab_dir, lab, role, reg, logger):
    ''' use dockerfiles to determine the set of containers '''
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
        getDates(image, reg, lab, logger)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve creation dates of lab images.')
    parser.add_argument('-l', '--lab', action='store', help='Get dates for just this lab')
    parser.add_argument('-p', '--premaster', action='store_true', default=False, help='Get dates from premaster')
    parser.add_argument('-d', '--dockerhub', action='store_true', default=False, help='Get dates from dockerhub')
    args = parser.parse_args()
    src_path = '../'
    labtainer_config_file = os.path.join(src_path, 'config', 'labtainer.config')
    logger = LabtainerLogging.LabtainerLogging("labtainer-publish.log", 'publish', labtainer_config_file)
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config_file, logger)
    labutils.logger = logger
    labdir = os.path.join(os.getenv('LABTAINER_DIR'), 'labs')
    mycwd = os.getcwd()
    os.chdir(labdir)
    cmd = 'git ls-files ./ | cut -d/ -f1 | uniq'
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = child.communicate()
    lab_list = output[0].decode('utf-8').strip().splitlines()
    os.chdir(mycwd)
    if args.dockerhub:
       registry = labtainer_config.default_registry
       print('Get registry dates from Docker Hub')
    elif not args.premaster:
       branch, registry = registry.getBranchRegistry()
       print('Get registry dates for branch %s from %s' % (branch, registry))
    else:
       registry = labtainer_config.test_registry
       print('Get registry dates for PREMASTER from %s' % (registry))
    if args.lab == None:
        skip_labs = 'skip-labs'
        skip = []
        with open(skip_labs) as fh:
            for line in fh:
                f = os.path.basename(line).strip()
                skip.append(f) 
        for lab in sorted(lab_list):
            lab = lab.strip()
            if lab not in skip:
                doLab(labdir, lab, 'student', registry, logger)
    else:
        doLab(labdir, args.lab, 'student', registry, logger)
    
