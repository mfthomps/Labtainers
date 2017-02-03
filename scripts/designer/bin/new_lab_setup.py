#!/usr/bin/env python
import os
import shutil
import glob
SEED_DIR=None
try:
    SEED_DIR = os.environ['SEED_DIR']
except:
    print('SEED_DIR environment variable not set.')
    exit(1)

tdir = os.path.join(SEED_DIR, 'scripts','designer','templates')
template_dirs = os.listdir(tdir)
here = os.getcwd()
labname = os.path.basename(here)
for source in template_dirs:
    print('copying %s' %  source)
    try:
        shutil.copytree(os.path.join(tdir, source), os.path.join(here, source)) 
    except:
        print('error copying %s to %s, expected %s to be empty' % (source, here, here))
        exit(1)

adapt_list = glob.glob(here+'/*/*template*')
for a in adapt_list:
    new = a.replace('template', labname)
    shutil.move(a, new)
