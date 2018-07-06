#!/usr/bin/env python
import subprocess
import sys
import os

lab = sys.argv[1]
cmd = 'docker ps -a'
ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
output = ps.communicate()
lab_container = ' %s.' % lab
container_list = []
for line in output[0].splitlines():
    #print line
    if lab_container in line:
        container_list.append(line.split()[0]) 
if len(container_list) > 0:
    cmd = 'docker rmi -f %s' % ' '.join(container_list)
    print cmd
    os.system(cmd)


lab = sys.argv[1]
cmd = 'docker images'
ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
output = ps.communicate()
image_find = '/%s.' % lab
image_find2 = '%s.' % lab
image_list = []
for line in output[0].splitlines():
    #print line
    if (image_find in line or line.startswith(image_find2)) and ' <none> ' not in line:
        image_list.append(line.split()[0]) 
if len(image_list) > 0:
    cmd = 'docker rmi -f %s' % ' '.join(image_list)
    print cmd
    os.system(cmd)
