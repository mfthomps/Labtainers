#!/usr/bin/env python

# Filename: redo.py
# Description:
# For lab development testing workflow.  This will stop containers of a lab, create or update lab images
# and start the containers.
#

import os
import subprocess
import sys
import ParseStartConfig
import start
import stop
import time
import datetime

LABS_ROOT = os.path.abspath("../../labs/")

def FileModLater(ts, fname):
    ''' is the given file later than the timestamp (which is in UTC)? '''
    df_time = os.path.getmtime(fname)
    #print('df ts %s' % df_time)

    df_string = datetime.datetime.fromtimestamp(df_time)
    #print('df_local time is %s' % df_string)

    df_utc_string = str(datetime.datetime.utcfromtimestamp(df_time))
    parts = df_utc_string.split('.')
    df_ts = time.mktime(time.strptime(parts[0], "%Y-%m-%d %H:%M:%S"))

    #print('df_utc time is %s' % df_utc_string)
    #print('df_utc ts is %s' % df_ts)
    if df_ts > ts:
        return True
    else:
        return False

def CheckBuild(labname, image_name, container_name, name):
    '''
    Determine if a container image needs to be rebuilt.
    '''
    retval = False
    print('check build for container %s image %s' % (container_name, image_name))
    cmd = "docker inspect -f '{{.Created}}' %s" % image_name
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result = child.stdout.read().strip()
    if 'Error:' in result or len(result.strip()) == 0:
        return True
    print('result is %s' % result)
    parts = result.strip().split('.')
    time_string = parts[0]
    #print('image time string %s' % time_string)
    ts = time.mktime(time.strptime(time_string, "%Y-%m-%dT%H:%M:%S"))
    #print('image ts %s' % ts)
    lab_path = os.path.join(LABS_ROOT,labname)
    df_name = 'Dockerfile.%s' % container_name
    df = os.path.join(lab_path, 'dockerfiles', df_name)
    if FileModLater(ts, df):
        print('dockerfile changed, would build')
        retval = True
    else:
        container_dir = os.path.join(lab_path, name)
        #print('container dir %s' % container_dir)
        for folder, subs, files in os.walk(container_dir):
            for f in files:
               f_path = os.path.join(folder, f)
               if FileModLater(ts, f_path):
                   print('%s is later, would build' % f_path)
                   retval = True
                   break
    return retval

def RedoLab(labname):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, "student")
    stop.StopLab(labname)
    for name, container in start_config.containers.items():
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        cmd = 'docker rm %s' % mycontainer_name
        os.system(cmd)
        if CheckBuild(labname, mycontainer_image_name, mycontainer_name, name):
            cmd = './buildImage.sh %s' % labname 
            os.system(cmd)
    start.StartLab(labname)


# Usage: redo.py <labname>
# Arguments:
#    <labname> - the lab to stop, delete and start
def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: redo.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    RedoLab(labname)

    return 0

if __name__ == '__main__':
    sys.exit(main())

