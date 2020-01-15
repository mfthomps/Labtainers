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
import registry
import VersionInfo

'''
Make all the Labtainer base files based on dates of their docker files,
and publish to registry of current branch.
'''
def doBase(image_name, registry):
    image_ext = image_name.split('.',1)[1]
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
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rebuild all Labtainer base images (if their Dockerfiles are newer than the base image)')
    labtainer_dir = os.getenv('LABTAINER_DIR')
    labtainer_config_file = os.path.join(labtainer_dir, 'config', 'labtainer.config')
    logger = LabtainerLogging.LabtainerLogging("/tmp/mkbases.log", 'publish', labtainer_config_file)
    labutils.logger = logger
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config_file, logger)
    
    branch, registry = registry.getBranchRegistry()
    
    dfile = os.path.abspath('../base_dockerfiles')
    base_list = os.listdir(dfile)
    
    exempt_file = 'exempt.txt'
    exempt_list = []
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
            image_info = labutils.imageInfo(image_name, registry, labtainer_config)
            if image_info is None:
                print('No image info for %s, rebuild' % image_name)
                logger.debug('No image info for %s  rebuild' % image_name)
                doBase(image_name, registry)
                continue
            x=parse(image_info.creation)
            ts = calendar.timegm(x.timetuple())
            #print('image ts %s  %s' % (ts, image_info.creation))
            if labutils.FileModLater(ts, full):
                print('WOUlD REBUILD %s' % image_name)
                logger.debug('WOUlD REBUILD %s' % image_name)
                doBase(image_name, registry)


