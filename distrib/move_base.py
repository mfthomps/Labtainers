#!/usr/bin/env python3
import sys
import os
sys.path.append('../scripts/labtainer-student/bin')
import RemoteBase
import LabtainerLogging
import ParseLabtainerConfig
import LabtainerBase
config_file = '../config/labtainer.config'
labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(config_file, None)
lgr = LabtainerLogging.LabtainerLogging("/tmp/move_base.log", 'none', config_file)
base_names = LabtainerBase.getBaseList(skip_exempt=False)

old_reg = 'mfthomps'
new_reg = 'labtainers'
os.system('docker login -u mfthomps')
for base in base_names:
    old = '%s/%s' % (old_reg, base)
    new = '%s/%s' % (new_reg, base)
    print(base)
    new_created, new_user = RemoteBase.inspectRemote(new, lgr)
    if new_created is not None:
        old_created, old_user = RemoteBase.inspectRemote(old, lgr)
    if new_created is None or old_created > new_created:
            cmd = 'docker pull %s' % (old)
            print(cmd)
            os.system(cmd)
            cmd = 'docker tag %s %s' % (old, new)
            print(cmd)
            os.system(cmd)
            cmd = 'docker push %s' % (new)
            print(cmd)
            os.system(cmd)
    else:
            print('new registry for %s is up to date.' % new)
