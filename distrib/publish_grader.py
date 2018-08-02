#!/usr/bin/env python
import os
import sys
import argparse
sys.path.append('../scripts/labtainer-student/bin')
import labutils
import ParseLabtainerConfig
import LabtainerLogging
import VersionInfo
def relabel(image, version, base_image, base_id, registry):
    with open('./dfile', 'w') as fh:
        fh.write('FROM %s\n' % image)
        fh.write('ARG version\n')
        fh.write('LABEL version=%s\n' % version)
        fh.write('LABEL base=%s.%s' % (base_image, base_id))

    cmd = 'docker build -f dfile -t %s.tmp .' % image
    os.system(cmd)
    cmd = 'docker tag %s.tmp %s/%s' % (image, registry, image)
    print cmd
    os.system(cmd)
    cmd = 'docker push %s/%s' % (registry, image)
    print cmd
    os.system(cmd)
    cmd = 'docker tag %s.tmp %s/%s:base_image%s' % (image, registry, image, base_id)
    print cmd
    os.system(cmd)
    cmd = 'docker push %s/%s:base_image%s' % (registry, image, base_id)
    print cmd
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

    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config_file, logger)
    if args.test_registry:
        registry = labtainer_config.test_registry
    else:
        registry = labtainer_config.default_registry
    dfile_path = '../scripts/designer/base_dockerfiles/Dockerfile.labtainer.grader'
    image_base = VersionInfo.getFrom(dfile_path, registry)
    base_id = VersionInfo.getImageId(image_base)
    framework_version = labutils.framework_version
    relabel('labtainer.grader', framework_version, image_base, base_id, registry)
    


if __name__ == '__main__':
    sys.exit(main())

