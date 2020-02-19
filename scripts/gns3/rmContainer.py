#!/usr/bin/env python3
import sys
import subprocess
import shlex
def findContainers(lab):
    cmd = 'docker ps -a'
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) > 0:
        logger.error('No containers: error returned %s, return false' % output[1])
        return None
    lookfor = ' %s_' % lab
    retval = []
    for line in output[0].decode('utf-8').splitlines():
        if lookfor in line:
            parts = line.split()
            retval.append(parts[0])          
    return retval

def rmContainer(cid):
    cmd = 'docker rm %s' % cid
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) > 0:
        logger.error('%s' % output[1])

if len(sys.argv) != 2:
    print('Will remove all containers for a given lab name. Usage:')
    print('\trmContainer lab')
    exit(1)
clist = findContainers(sys.argv[1])
for c in clist:
    print('remove container: %s' % c)
    rmContainer(c)
