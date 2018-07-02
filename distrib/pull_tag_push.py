#!/usr/bin/env python
import os
import sys
import argparse
sys.path.append('../scripts/labtainer-student/bin')
import InspectLocalReg
import InspectRemoteReg
'''
Pull all labtainer container images from the docker hub, retag them, and push to a 
local registry.  Only replace the local registry if its image is older than the remote.
'''

def do_lab(lab_dir, lab, role, source_reg, dest_reg, force):
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
        except:
            print('could not get image from %s' % df);
            continue
        local_created, local_user, version, tag = InspectLocalReg.inspectLocal(image, dest_reg)
        if local_created is not None:
            remote_created, remote_user, version, tag = InspectRemoteReg.inspectRemote(image)
        if force or local_created is None or remote_created > local_created:
            cmd = 'docker pull %s/%s' % (source_reg, image)
            #print cmd
            os.system(cmd)
            cmd = 'docker tag %s/%s %s/%s' % (source_reg, image, dest_reg, image)
            #print cmd
            os.system(cmd)
            cmd = 'docker push %s/%s' % (dest_reg, image)
            #print cmd
            os.system(cmd)
        else:
            print('local registry for %s is up to date.' % image)

parser = argparse.ArgumentParser(description='pull from the docker hub and push to local registry')
parser.add_argument('-l', '--lab', action='store', help='only pull/tag/push this lab')
parser.add_argument('-f', '--force', action='store_true', default=False, help='force pull/push')
args = parser.parse_args()
skip = []
with open('skip-labs') as fh:
   for line in fh:
       f = os.path.basename(line).strip()
       print('will skip [%s]' % f)
       skip.append(f)

labdir = '../labs'
lab_list = os.listdir(labdir)
#
# test with a single lab.  Then use loop below once it works.
#
testregistry = 'testregistry:5000'
if args.lab is not None:
    do_lab(labdir, args.lab, 'student', 'mfthomps', testregistry, args.force)
    do_lab(labdir, args.lab, 'instructor', 'mfthomps', testregistry, args.force)
else:
    #print('commented out for now')
    testregistry = 'testregistry:5000'
    for lab in sorted(lab_list):
        if lab not in skip:
            do_lab(labdir, lab, 'student', 'mfthomps', testregistry, args.force)
            do_lab(labdir, lab, 'instructor', 'mfthomps', testregistry, args.force)
