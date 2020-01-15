#!/usr/bin/env python3
import subprocess
import argparse
import os
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='removebase', description='Remove all local registry instances of a base image')
    parser.add_argument('base',  help='Name of the base to remove')
    args = parser.parse_args()
    if True: 
        cmd = 'docker images'
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        image_list = []
        for line in output[0].decode('utf-8').splitlines():
            #print(line)
            if (args.base in line) and ' <none> ' not in line:
                parts = line.split()
                image = '%s:%s' % (parts[0], parts[1])
                image_list.append(image)
        if len(image_list) > 0:
            cmd = 'docker rmi -f %s' % ' '.join(image_list)
            #print(cmd)
            os.system(cmd)
        else:
            print('No images for %s' % lab)

