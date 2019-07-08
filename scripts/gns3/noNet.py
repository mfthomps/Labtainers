#!/usr/bin/env python
import sys
import os
import argparse
from netaddr import IPNetwork
labtainer_dir = os.getenv('LABTAINER_DIR')
if labtainer_dir is None:
    print('Must define LABTAINER_DIR environment variable')
    exit(1)
sys.path.append(os.path.join(labtainer_dir, 'scripts', 'labtainer-student','bin'))
sys.path.append(os.path.join(labtainer_dir, 'scripts', 'labtainer-student','lab_bin'))
import labutils
import LabtainerLogging

'''
Modify the images from a Labtainers lab to remove all files under /etc/network (inclusive).
GNS3 will mount container specific files at /etc/network, and thus we must remove any such
from Labtainers.  
The resulting image name will be <lab name>-<component>-<labtainer>, and that image should then
be imported into GNS3 as a Docker container image.
'''

gns3_path = '/home/mike/GNS3/projects'
labtainers_path = '/home/mike/labtainer/trunk/labs'
parser = argparse.ArgumentParser(description='Create gns3-friendy variants of Labtainers images.')
parser.add_argument('labname', help='Name of labtainers lab')
args = parser.parse_args()

labutils.logger = LabtainerLogging.LabtainerLogging("noNet.log", 'eh', "../../config/labtainer.config")

tdir = '/tmp/nonet'
try:
    os.mkdir(tdir)
except:
    pass

labtainer_lab = os.path.join(labtainers_path, args.labname)
labtainer_config, start_config = labutils.GetBothConfigs(labtainer_lab, labutils.logger)
for name, container in start_config.containers.items():
    os.system('rm -fr /tmp/nonet/*')
    fname = 'Dockerfile.%s-%s' % (args.labname, name)
    full = os.path.join(tdir, fname)
    with open(full, 'w') as fh:
        full = '%s/%s' % (container.registry, container.image_name)
        print('container image for %s is %s' % (name, full))
        line = 'FROM %s' % full
        fh.write(line+'\n')
        fh.write('USER root\n')
        fh.write('RUN rm -fr /etc/network\n')
    os.chdir(tdir)
    image = '%s-%s-labtainer' % (args.labname, name)
    cmd = 'docker build -f %s -t %s .' % (fname, image)
    os.system(cmd)
