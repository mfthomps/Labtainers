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

home = os.getenv("HOME")
gns3_path = os.path.join(home, 'GNS3', 'projects')
labtainers_path = os.path.join(labtainer_dir, 'labs')
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
created_images = []
for name, container in start_config.containers.items():
    os.system('rm -fr /tmp/nonet/*')
    fname = 'Dockerfile.%s-%s' % (args.labname, name)
    full = os.path.join(tdir, fname)
    from_image = container.image_name
    created, user, version = labutils.inspectImage(from_image)
    if created is None:
        labutils.logger.error("Running noNet.py and cannot find image %s locally." % from_image)
        from_image = '%s/%s' % (container.registry, container.image_name)
        created, user, version = labutils.inspectImage(from_image)
        if created is None:
            labutils.logger.error("Running noNet.py and cannot find image %s in remote registry." % from_image)

    print('container image for %s is %s' % (name, from_image))
    with open(full, 'w') as fh:
        line = 'FROM %s' % from_image
        fh.write(line+'\n')
        fh.write('USER root\n')
        fh.write('RUN rm -fr /etc/network\n')
    os.chdir(tdir)
    image = '%s_%s-labtainer' % (args.labname, name)
    created_images.append(image)
    cmd = 'docker build -f %s -t %s .' % (fname, image)
    os.system(cmd)
print('-----------------------------------------------------------')
print('[Use the images below to define Docker container templates')
print(' for use in your lab in GNS3.]:')
for img in created_images:
    print('- %s' % img)
