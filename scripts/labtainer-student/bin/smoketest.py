#!/usr/bin/env python
import subprocess
import os

def checkLab(lab):
    retval = True
    cmd = 'start.py -q %s' % lab
    ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1]) > 0:
        print('%s' % output[0])
        print('%s' % output[1])
        retval = False

    cmd = 'stop.py %s' % lab
    ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1]) > 0:
        print('%s' % output[0])
        print('%s' % output[1])
        retval = False
    return retval

def checkAll():
    
    skip_labs = os.path.abspath('../../../distrib/skip-labs')
    skip = []
    if os.path.isfile(skip_labs):
        with open(skip_labs) as fh:
            for line in fh:
                f = os.path.basename(line).strip()
                print('adding [%s]' % f)
                skip.append(f)

    
    lab_parent = os.path.abspath('../../labs')
    lab_list = os.listdir(lab_parent)
    for lab in lab_list:
        if lab in skip:
            continue
        result = checkLab(lab)
        if not result:
            exit(1)


checkAll()
