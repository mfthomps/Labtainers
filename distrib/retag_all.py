#!/usr/bin/env python
import os
import sys
import argparse
sys.path.append('../scripts/labtainer-student/bin')
import InspectLocalReg
import InspectRemoteReg
import VersionInfo
import labutils
import subprocess
'''
Retag all labtainer images to include their base image id, and include the base
image name in a label.
'''
    
def do_lab(lab_dir, lab, role, registry):
    framework_version = labutils.framework_version 
    ''' use docker files to identify each docker image to relabel '''
    docker_dir = os.path.join(lab_dir, lab, 'dockerfiles')
    if not os.path.isdir(docker_dir):
        print('%s not a directory' % docker_dir)
        return
    df_list = [f for f in os.listdir(docker_dir) if os.path.isfile(os.path.join(docker_dir, f))]
    for df in df_list:
        if df.endswith('.swp'):
            continue
        dfile_path = os.path.join(docker_dir,df)
        ''' get the image name from the docker file '''
        image_base = VersionInfo.getFrom(dfile_path, registry)
        ''' get the base identifier of the image present on this installation for that image '''
        base_id = VersionInfo.getImageId(image_base)
        try:
            parts = df.split('.')
            image = '%s.%s.%s' % (parts[1], parts[2], role)
        except:
            print('could not get image from %s' % df);
            continue
        cmd = './relabel.sh %s %s %s %s %s' % (registry, framework_version , image, image_base, base_id)
        print cmd
        os.system(cmd)

def main():
    parser = argparse.ArgumentParser(description='Build the images labs and publish to a registry')
    parser.add_argument('-l', '--lab', action='store', help='retag just this lab')
    parser.add_argument('-t', '--test_registry', action='store_true', default=False, help='build and publish with test registry')
    skip = []
    with open('skip-labs') as fh:
       for line in fh:
           f = os.path.basename(line).strip()
           #print('will skip [%s]' % f)
           skip.append(f)
    
    labdir = '../labs'
    lab_list = os.listdir(labdir)
    #
    # test with a single lab.  Then use loop below once it works.
    #
    args = parser.parse_args()
    registry = 'mfthomps'
    if args.test_registry:
        registry = 'testregistry:5000'
    if args.lab is not None:
        print('retag lab %s' % args.lab)
        do_lab(labdir, args.lab, 'student', registry)
    else:
        #print('commented out for now')
        for lab in sorted(lab_list):
            if lab not in skip:
                do_lab(labdir, lab, 'student', registry)
if __name__ == '__main__':
    sys.exit(main())
