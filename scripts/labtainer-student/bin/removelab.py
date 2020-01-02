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
    for line in output[0].decode('utf-8').splitlines():
        if lab_container in line or gns3_container in line :
            container_list.append(line.split()[0]) 
    if len(container_list) > 0:
        cmd = 'docker rm %s' % ' '.join(container_list)
        #print(cmd)
        os.system(cmd)
    
    if not justContainers: 
        cmd = 'docker images'
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        image_find = '/%s.' % lab
        image_find2 = '%s.' % lab
        image_find3 = '%s_' % lab
        image_list = []
        for line in output[0].decode('utf-8').splitlines():
            #print line
            if (image_find in line or line.startswith(image_find2) or line.startswith(image_find3)) and ' <none> ' not in line:
                parts = line.split()
                image = '%s:%s' % (parts[0], parts[1])
                image_list.append(image)
        if len(image_list) > 0:
            cmd = 'docker rmi -f %s' % ' '.join(image_list)
            #print(cmd)
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
