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
import labutils
import ParseLabtainerConfig
import LabtainerLogging
import VersionInfo
import registry
def relabel(image, version, base_image, base_id, registry):
    with open('./dfile', 'w') as fh:
        fh.write('FROM %s\n' % image)
        fh.write('ARG version\n')
        fh.write('LABEL version=%s\n' % version)
        fh.write('LABEL base=%s.%s' % (base_image, base_id))

    cmd = 'docker build -f dfile -t %s.tmp .' % image
    os.system(cmd)
    '''
    cmd = 'docker tag %s.tmp %s/%s' % (image, registry, image)
    #print cmd
    os.system(cmd)
    cmd = 'docker push %s/%s' % (registry, image)
    #print cmd
    os.system(cmd)
    '''
    cmd = 'docker tag %s.tmp %s/%s:base_image%s' % (image, registry, image, base_id)
    #print cmd
    os.system(cmd)
    cmd = 'docker push %s/%s:base_image%s' % (registry, image, base_id)
    #print cmd
    os.system(cmd)

def main():
    parser = argparse.ArgumentParser(description='Build and publish the grader')
    parser.add_argument('-t', '--test_registry', action='store_true', help='Use image from test registry')
    args = parser.parse_args()
    if args.test_registry:
        if os.getenv('TEST_REGISTRY') is None:
            print('use putenv to set it')
            os.putenv("TEST_REGISTRY", "TRUE")
            ''' why does putenv not set the value? '''
            os.environ['TEST_REGISTRY'] = 'TRUE'
        else:
            print('exists, set it true')
            os.environ['TEST_REGISTRY'] = 'TRUE'
        print('set TEST REG to %s' % os.getenv('TEST_REGISTRY'))
    here = os.getcwd()
    os.chdir('../scripts/designer/bin')
    test_registry = ''
    if args.test_registry:
        test_registry = '-t'
    cmd = './create_image.sh grader %s' % test_registry
    os.system(cmd)
    os.chdir(here)
    src_path = '../'
    labtainer_config_file = os.path.join(src_path, 'config', 'labtainer.config')
    logger = LabtainerLogging.LabtainerLogging("publish_grader.log", 'publish', labtainer_config_file)
    labutils.logger = logger

    if args.test_registry:
        branch, use_registry = registry.getBranchRegistry()
    else:
        labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config_file, logger)
        use_registry = labtainer_config.default_registry
    dfile_path = '../scripts/designer/base_dockerfiles/Dockerfile.labtainer.grader'
    image_base = VersionInfo.getFrom(dfile_path, use_registry)
    base_id = VersionInfo.getImageId(image_base, True)
    framework_version = labutils.framework_version
    relabel('labtainer.grader', framework_version, image_base, base_id, use_registry)
    


if __name__ == '__main__':
    sys.exit(main())

