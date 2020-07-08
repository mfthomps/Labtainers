#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
import calendar
from dateutil import parser
from dateutil.parser import parse
sys.path.append('../../labtainer-student/bin')
import LabtainerLogging
import ParseLabtainerConfig
import labutils
import rebuild
import registry
import VersionInfo

'''
Make all the Labtainer base files based on dates of their docker files,
and publish to registry of current branch.
'''
def rmBase(image_name, registry):
    cmd = 'docker images'
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    image_list = []
    look_for = '%s/%s' % (registry, image_name)
    no_reg = '%s ' % image_name
    print('look for %s   or %s' % (look_for, no_reg))
    for line in output[0].decode('utf-8').splitlines():
        #print(line)
        if (look_for in line) and ' <none> ' not in line:
            parts = line.split()
            image = '%s:%s' % (parts[0], parts[1])
            image_list.append(image)
        elif (line.startswith(no_reg)) and ' <none> ' not in line:
            image_list.append(image_name)
    if len(image_list) > 0:
        cmd = 'docker rmi -f %s' % ' '.join(image_list)
        print(cmd)
        os.system(cmd)
    else:
        print('No images for %s' % image_name)

def doBase(image_name, registry):
    image_ext = image_name.split('.',1)[1]
    if image_name == 'labtainer.bird':
        cmd = './create_bird_image.sh -f'
    else:
        cmd = './create_image.sh %s -f' % image_ext
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    image_list = []
    for line in output[0].decode('utf-8').splitlines():
        print(line)
    for line in output[1].decode('utf-8').splitlines():
        print(line)
    if len(output[1]) == 0:
        cmd = 'docker tag %s %s/%s' % (image_name, registry, image_name)
        os.system(cmd)
        cmd = 'docker push %s/%s' % (registry, image_name)
        os.system(cmd)
    else:
        print('Error creating image %s, exit' % image_name)
        exit(1)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rebuild all Labtainer base images (if their Dockerfiles are newer than the base image)')
    parser.add_argument('-n', '--no_build', action='store_true', default=False, help='Do not rebuild, just report on what would be built, HOWEVER local images may be deleted.')
    args = parser.parse_args()
    labtainer_dir = os.getenv('LABTAINER_DIR')
    labtainer_config_file = os.path.join(labtainer_dir, 'config', 'labtainer.config')
    logger = LabtainerLogging.LabtainerLogging("/tmp/mkbases.log", 'publish', labtainer_config_file)
    labutils.logger = logger
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config_file, logger)
    
    branch, registry = registry.getBranchRegistry()
    
    dfile = os.path.abspath('../base_dockerfiles')
    workspace = os.path.abspath('../workspace')
    base_list = os.listdir(dfile)
    
    exempt_file = 'exempt.txt'
    exempt_list = []
    logger.debug('mkbases branch %s, registry %s' % (branch, registry))
    with open(exempt_file) as fh:
        for line in fh:
            exempt_list.append(line.strip()) 
    for base in base_list:
        if base.startswith('Dockerfile'):
            full = os.path.join(dfile, base)
    
            image_name = base.split('.',1)[1]
            image_ext = image_name.split('.',1)[1]
            #print(image_name) 
            if image_name in exempt_list:
                print('skipping %s, is exempt' % image_name)
                logger.debug('skipping %s, is exempt' % image_name)
                continue
            rmBase(image_name, registry)
            image_info = labutils.imageInfo(image_name, registry, registry, labtainer_config)
            if image_info is None:
                print('No image info for %s, rebuild' % image_name)
                logger.debug('No image info for %s  rebuild' % image_name)
                if not args.no_build:
                    doBase(image_name, registry)
                    logger.debug('Did rebuild of %s' % image_name)
                continue
            x=parse(image_info.creation)
            ts = calendar.timegm(x.timetuple())
            logger.debug('image %s ts %s  %s' % (image_name, ts, image_info.creation))
            if rebuild.FileModLater(ts, full):
                print('WOUlD REBUILD %s' % image_name)
                logger.debug('WOUlD REBUILD %s' % image_name)
                if not args.no_build:
                    doBase(image_name, registry)
            else:
                with open(full) as docker_file:
                    for line in docker_file:
                        print('line is %s' % line)
                        if line.startswith('ADD'):
                            print('is add')
                            parts = line.split()
                            from_file = parts[1].strip()
                            if from_file.startswith('system'):
                                full_from = os.path.join(workspace, from_file)
                                print('full_from is %s' % full_from)
                                if rebuild.FileModLater(ts, full_from):
                                    print('%s later, WOUlD REBUILD %s' % (full_from, image_name))
                                    logger.debug('WOUlD REBUILD %s' % image_name)
                                    if not args.no_build:
                                        doBase(image_name, registry)
                                        break 


