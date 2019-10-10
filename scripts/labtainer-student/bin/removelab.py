#!/usr/bin/env python
import subprocess
import sys
import os
import argparse

def removeLab(lab, justContainers=False):
    cmd = 'docker ps -a'
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if lab == 'GNS3':
        lab_container = '/gns3/init.sh'
    else:
        lab_container = ' %s.' % lab
    gns3_container = ' %s_' % lab
    container_list = []
    for line in output[0].splitlines():
        #print line
        if lab_container in line or gns3_container in line :
            container_list.append(line.split()[0]) 
    if len(container_list) > 0:
        cmd = 'docker rm %s' % ' '.join(container_list)
        print cmd
        os.system(cmd)
    
    if not justContainers: 
        cmd = 'docker images'
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        image_find = '/%s.' % lab
        image_find2 = '%s.' % lab
        image_find3 = '%s_' % lab
        image_list = []
        for line in output[0].splitlines():
            #print line
            if (image_find in line or line.startswith(image_find2) or line.startswith(image_find3)) and ' <none> ' not in line:
                parts = line.split()
                image = '%s:%s' % (parts[0], parts[1])
                image_list.append(image)
        if len(image_list) > 0:
            cmd = 'docker rmi -f %s' % ' '.join(image_list)
            print cmd
            os.system(cmd)
        else:
            print('No images for %s' % lab)

def main():
    parser = argparse.ArgumentParser(prog='removelab', description='Remove a lab and its images from a Labtainers installation. \
        The next time the lab is run, a fresh (updated) image will be pulled.')
    parser.add_argument('labname', default='NONE', nargs='?', action='store', help='The lab to delete.  A value of "GNS3" will delete all GNS labs.')
    parser.add_argument('-c', '--containers', action='store_true', help='Delete the containers of this lab, but do not delete the images.')
    args = parser.parse_args()
    removeLab(args.labname, args.containers)

if __name__ == '__main__':
    sys.exit(main())
