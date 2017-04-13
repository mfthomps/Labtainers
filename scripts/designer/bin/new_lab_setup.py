#!/usr/bin/env python
import os
import shutil
import glob
import pwd
'''
Copy a set of initial lab configuration files into a new lab and
adjust their names and content to reflect the lab name.
'''
LABTAINER_DIR=None
try:
    LABTAINER_DIR = os.environ['LABTAINER_DIR']
except:
    print('LABTAINER_DIR environment variable not set.')
    exit(1)

tdir = os.path.join(LABTAINER_DIR, 'scripts','designer','templates')
template_dirs = os.listdir(tdir)
here = os.getcwd()
labname = os.path.basename(here)
config_dir = None
for source in template_dirs:
    if source == 'bin':
        os.mkdir(labname)
        try:
            shutil.copytree(os.path.join(tdir, source), os.path.join(here, labname, source)) 
        except:
            print('error copying %s to %s, expected %s to be empty' % (source, here, here))
            exit(1)
        
    print('copying %s' %  source)
    try:
        shutil.copytree(os.path.join(tdir, source), os.path.join(here, source)) 
    except:
        print('error copying %s to %s, expected %s to be empty' % (source, here, here))
        exit(1)

''' alter template file names, except those that will have altered content '''
start_config_template = 'config/start.config.template'
start_config_file = 'config/start.config'
adapt_list = glob.glob(here+'/*/*template*')
for a in adapt_list:
    if not a.endswith(start_config_template):
        new = a.replace('template', labname)
        shutil.move(a, new)

default_string = 'default'
seed_label = 'LAB_MASTER_SEED'
myname = pwd.getpwuid(os.getuid()).pw_name
with open(start_config_template) as fh:
  with open(start_config_file, 'w') as out_fh:
    for line in fh:
        if line.strip().startswith(seed_label):
            out_fh.write('\t%s %s_%s_master_seed\n' % (seed_label, labname, myname))
        elif not line.strip().startswith('#') and default_string in line:
            new_line = line.replace(default_string, labname)
            out_fh.write(new_line)
        else:
            out_fh.write(line)
os.remove(start_config_template) 
