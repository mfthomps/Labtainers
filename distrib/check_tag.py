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
import labutils
'''
Compare all labtainer image base labels with when would be expected based
on the docker file.  Fix the ones that are not consistent.
'''
    
def do_lab(lab_dir, lab, role, registry):
    framework_version = labutils.framework_version 
    docker_dir = os.path.join(lab_dir, lab, 'dockerfiles')
    if not os.path.isdir(docker_dir):
        print('%s not a directory' % docker_dir)
        return
    print('LAB: %s' % lab)
    df_list = [f for f in os.listdir(docker_dir) if os.path.isfile(os.path.join(docker_dir, f))]
    for df in df_list:
        if df.endswith('.swp'):
            continue
        dfile_path = os.path.join(docker_dir,df)
        image_base = VersionInfo.getFrom(dfile_path, registry)
        print('image base from %s is %s' % (dfile_path, image_base))
        base_id = VersionInfo.getImageId(image_base)
        try:
            parts = df.split('.')
            image = '%s.%s.%s' % (parts[1], parts[2], role)
        except:
            print('could not get image from %s' % df);
            continue
        print('image: %s expect base %s' % (image, image_base))
        created, user, version, use_tag, base = InspectLocalReg.inspectLocal(image, registry, True)
        print('created: %s user: %s version: %s tag %s base %s' % (created, user, version, use_tag, base))
        if not base.startswith(image_base):
            cmd = './relabel.sh %s %s %s %s %s' % (registry, framework_version , image, image_base, base_id)
            print("MISMATCH")
            print cmd
            os.system(cmd)
            


def main():
    parser = argparse.ArgumentParser(description='Build the images labs and publish to a registry')
    parser.add_argument('-l', '--lab', action='store', help='retag just this lab')
    parser.add_argument('-t', '--test_registry', action='store_true', default=False, help='build and publish with test registry')
    parser.add_argument('-s', '--start', action='store', help='start with lab')
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
        do_lab(labdir, args.lab, 'instructor', registry)
    else:
        #print('commented out for now')
        for lab in sorted(lab_list):
            if lab not in skip:
                if args.start is not None and lab < args.start:
                    continue
                do_lab(labdir, lab, 'student', registry)
                do_lab(labdir, lab, 'instructor', registry)
if __name__ == '__main__':
    sys.exit(main())
