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
import sys
import os
import subprocess
import shlex
import glob
import argparse
from dateutil import parser
from dateutil.parser import parse
import calendar
import datetime
import time

import labutils
import logging
import LabtainerLogging 
import CurrentLab
import registry
import CheckTars
import BigFiles
import BigExternal

try:
    from dateutil import parser
except:
    print('Lab building now requires a python3 environment with includes dateutil')
    print('Please migrate to a newer Linux distribution, e.g, Ubuntu 18')
    print('As a short-term work-around, use the rebuild command (no .py suffix) to reference python2')
    print('Avoid use of python 3.5.2, it is broken, see our README.')
    exit(1)

class RegistryInfo():
    def __init__(self, name, image_name, registry, base_registry):
        self.name = name
        self.image_name = image_name
        self.registry = registry
        self.base_registry = base_registry

def DateIsLater(df_utc_string, ts, local=False, debug=False):
    parts = df_utc_string.split('.')
    ''' use dateutil to parse for zone, which we get from svn '''
    x=parse(parts[0])
    if local:
        df_ts = time.mktime(x.timetuple())
    else:
        df_ts = calendar.timegm(x.timetuple())
    if debug:
        labutils.logger.debug('df_utc time is %s' % df_utc_string)
        labutils.logger.debug('df_utc ts is %s given ts is %s' % (df_ts, ts))
    df_ts = int(df_ts)
    ts = int(ts)

    if df_ts > ts:
        ''' if over a four months old, and less than a week apart, assume build prior to commit '''
        now = int(time.time())
        since = (now - ts)
        diff_max = 604800 
        old_max = 86400*130
        if ((df_ts - ts) < diff_max) and (now - ts) > old_max:
            labutils.logger.debug('Less than a week dif and older than four months (%d), assume no change' % since)
            return False
        else:
            if debug:
                labutils.logger.debug('fd_ts - ts = %d  dif_max %d  now-ts=%d  old_max %d' % ((df_ts - ts), diff_max, (now-ts), old_max))
            return True
    else:
        return False

def EmptyTar(fname):
    size = os.path.getsize(fname)
    if size == 10240 or size == 110:
        return True
    else:
        return False

def FileModLater(ts, fname, big_list=[]):
    ''' is the given file later than the given timestamp?  Account for git dates, ie.g., don't let file date override git date '''
    retval = False
    df_utc_string = None
    # start with check of svn status
    #if os.path.isfile(fname):
    cmd = 'git ls-files -s %s' % fname
    child = subprocess.Popen(shlex.split(cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = child.communicate()
    if len(output[0].decode('utf-8').strip()) > 0:
        has_svn = True
    else:        
        has_svn = False
    #else:
    #    has_svn = False
    cmd = 'git status -s %s' % fname
    labutils.logger.debug('cmd: %s' % cmd)
    child = subprocess.Popen(shlex.split(cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = child.stdout.readline().decode('utf-8')
        line = line.strip()
        if line == '':
            break
        labutils.logger.debug('line: <%s>' % line)
        ''' ignore empty tar archives '''
        if line.startswith('?'):
            f = line.strip().split()[1]
            abspath = os.path.abspath(f)
            if abspath in big_list:
                labutils.logger.debug('FileModLater, is bigfile %s' % f)
                return False
            if os.path.isfile(fname):
                has_svn = False
            else:
                if abspath != fname:
                    has_svn = True
            if f.endswith('.tar'):
                if EmptyTar(f):
                    continue
                fdir = os.path.dirname(f)
                if os.path.isfile(os.path.join(fdir,'external-manifest')):
                    continue
            elif f.endswith('_tar') and os.path.isdir(f):
                continue
            elif os.path.isfile(f):
                df_time = os.path.getmtime(f)
                df_utc_string = str(datetime.datetime.utcfromtimestamp(df_time))
                labutils.logger.debug('df_time %s   string %s' % (df_time, df_utc_string))
                retval = DateIsLater(df_utc_string, ts)
                if retval:
                    break
        else:
            has_svn = True
         
        #logger.debug(line)
        if os.path.isdir(fname) or line.startswith('M') or line.startswith('>'):
            if '/home_tar/' in line or '/sys_tar/' in line:
                continue
            #logger.debug('svn status found something for fname %s, line %s' % (fname, line))
            if line.startswith('M'):
                file_path = line.split()[-1]
                df_time = os.path.getmtime(file_path)
                #parent = os.path.dirname(line.split()[1])
                #df_time = os.path.getmtime(parent)
            elif line.startswith('D'):
                file_path = line.split()[-1]
                if '/' in file_path:
                    file_dir = os.path.dirname(file_path)
                    while not os.path.isdir(file_dir):
                        file_dir = os.path.dirname(file_dir)
                    df_time = os.path.getmtime(file_dir)
            else:
                file_path = '/'+line.split('/', 1)[-1].strip()
                #logger.debug('not an "M" or D, get dftime for %s' % file_path)
                if not os.path.exists(file_path):
                    continue
                df_time = os.path.getmtime(file_path)
            df_utc_string = str(datetime.datetime.utcfromtimestamp(df_time))
            retval = DateIsLater(df_utc_string, ts, debug=False)
            if retval:
                break
    if df_utc_string is None:
        # try svn info.  stderr implies not in svn
        if not has_svn: 
            #logger.debug('not in svn?')
            # assume not in svn
            labutils.logger.debug("not in svn? %s" % fname)
            if fname.endswith('.tar'):
                if EmptyTar(fname):
                    # hacky special case for empty tar files.  ug.
                    return False
                fdir = os.path.dirname(fname)
                # why not consider tars built from external manifest???
                #if os.path.isfile(os.path.join(fdir,'external-manifest')):
                #    return False
            if os.path.isfile(fname):
                df_time = os.path.getmtime(fname)
            else:
                check_file = newest_file_in_tree(fname)
                labutils.logger.debug('FileModLater, not in svn latest found is %s' % check_file)
                if EmptyTar(check_file):
                    # hacky special case for empty tar files.  ug.
                    return False
                if os.path.basename(check_file) == 'sys_tar' or os.path.basename(check_file) == 'home_tar':
                    return False
                if check_file in big_list:
                    labutils.logger.debug('FileModLater, not in svn is bigfile %s' % check_file)
                    return False
                df_time = os.path.getmtime(check_file)
            df_utc_string = str(datetime.datetime.utcfromtimestamp(df_time))
            retval = DateIsLater(df_utc_string, ts)
        else:
            # in svn, look for changed date
            cmd = 'git log -1 --format="%%ad" %s' % fname
            labutils.logger.debug('in svn, look for changed date %s' % cmd)
            child = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = child.communicate()
            if len(output[0].decode('utf-8').strip()) > 0:
                df_utc_string = output[0].decode('utf-8').strip()
                svn_is_later = DateIsLater(df_utc_string, ts, local=True, debug=True)
                labutils.logger.debug('git log returned %s  is later? %r' % (df_utc_string, svn_is_later))
                df_time = os.path.getmtime(fname)
                file_utc_string = str(datetime.datetime.utcfromtimestamp(df_time))
                file_is_later = DateIsLater(file_utc_string, ts, local=False, debug=True)
                labutils.logger.debug('file time %s  is later? %r' % (file_utc_string, file_is_later))
                retval = svn_is_later and file_is_later

            if df_utc_string is None:
                # must be an add
                labutils.logger.debug('%s must be an add' % fname)
                if os.path.isfile(fname):
                    df_time = os.path.getmtime(fname)
                else:
                    check_file = newest_file_in_tree(fname)
                    labutils.logger.debug('latest found is %s' % check_file)
                    df_time = os.path.getmtime(check_file)
                df_utc_string = str(datetime.datetime.utcfromtimestamp(df_time))
                retval = DateIsLater(df_utc_string, ts, debug=False)

    ''' is the given file later than the timestamp (which is in UTC)? '''
    labutils.logger.debug('df ts %s' % df_time)
    return retval

def ImageExists(image_name, registry):
    '''
    determine if a given image exists.
    '''
    retval = True
    labutils.logger.debug('check existence of image %s registry %s' % (image_name, registry))
    cmd = "docker inspect -f '{{.Created}}' --type image %s" % image_name
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].decode('utf-8').strip()) > 0:
        if registry is not None:
            with_registry = '%s/%s' % (registry, image_name)
            return ImageExists(with_registry, None)
        else:
            labutils.logger.debug('No image: error returned %s, return false' % output[1].decode('utf-8'))
            return False, None, None
    result = output[0].decode('utf-8').strip()
    #logger.debug('result is %s' % result)
    if 'Error:' in result or len(result.strip()) == 0:
        if registry is not None:
            with_registry = '%s/%s' % (image_name, registry)
            return ImageExists(with_registry, None)
        else:
            if 'Error:' in result:
                labutils.logger.debug("Command was (%s)" % cmd)
                labutils.logger.debug("Error from command = '%s'" % result)
            return False, result, image_name
    return True, result, image_name

def BaseImageTime(dockerfile, registry):
    image_name = None
    retval = 0
    with open(dockerfile) as fh:
        for line in fh:
            if line.strip().startswith('FROM'):
                parts = line.strip().split()
                image_name = parts[1]
                if registry is not None:
                    image_name = image_name.replace("$registry", registry)
                elif '/' in image_name:
                    image_name = image_name.split('/')[1]
                break
    if image_name is None:
        labutils.logger.error('no base image found in %s' % dockerfile)
        exit(1)
    image_exists, result, dumb = ImageExists(image_name, None)
    if image_exists:
        parts = result.strip().split('.')
        #time_string = parts[0]
        #logger.debug('base image time string %s' % time_string)
        #retval = time.mktime(time.strptime(time_string, "%Y-%m-%dT%H:%M:%S"))
        x=parse(parts[0])
        retval = calendar.timegm(x.timetuple())
        labutils.logger.debug('base image time string %s returning %s' % (parts[0], retval))
    else:
        labutils.logger.debug('base image %s not found, assume not updated' % image_name)
    return retval, image_name
 
def newest_file_in_tree(rootfolder):
    if len(os.listdir(rootfolder)) > 0:
        try:
            return max(
                (os.path.join(dirname, filename)
                for dirname, dirnames, filenames in os.walk(rootfolder)
                for filename in filenames if not filename == 'home.tar' and not filename == 'sys.tar'),
                key=lambda fn: os.stat(fn).st_mtime)
        except ValueError:
            return rootfolder
    else:
        return rootfolder

def removeStrays(container_dir, name, labname):
    ''' remove any stray gz files from previous builds '''
    gmask = '/*.%s.student.tar.gz' % name
    gz_list = glob.glob(container_dir+gmask)
    for gz in gz_list:
        labutils.logger.debug('Stray gz %s will be deleted' % gz)
        os.remove(gz)
    gmask = '/Dockerfile.%s.%s.*' % (labname, name)
    #print('gmask %s' % (container_dir+gmask))
    df_list = glob.glob(container_dir+gmask)
    for df in df_list:
        labutils.logger.debug('Stray docker file %s will be deleted' % df)
        os.remove(df)

def GetBigFiles(lab_path):        
    big_list_file = os.path.join(lab_path,'config', 'bigexternal.txt')
    labutils.logger.debug('big_list_file at %s' % big_list_file)
    big_list = []
    if os.path.isfile(big_list_file):
        with open(big_list_file) as fh:
            for line in fh:
                if not line.strip().startswith('#') and len(line.strip())>0:
                    parts = line.split()
                    if len(parts) == 2:
                      
                        path = os.path.join(lab_path, parts[1])
                        labutils.logger.debug('adding to big_list %s' % path)
                        big_list.append(path)
    return big_list

def GetImageUser(image_name, container_registry):
    
    user = None
    password = None
    cmd = 'docker history --no-trunc %s' % image_name
    child = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = child.communicate()
    if len(output[1]) > 0:
        cmd = 'docker history --no-trunc %s/%s' % (container_registry, image_name)
        child = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = child.communicate()
    if len(output[0]) > 0:
        for line in output[0].decode('utf-8').splitlines(True):
            parts = line.split()
            for p in parts:
                if p.startswith('user_name='):
                    user = p.split('=')[1]
                elif p.startswith('password='):
                    password = p.split('=')[1]
            if user is not None:
                return user, password 
    return user, password
        

def CheckBuild(lab_path, image_name, image_info, container_name, name, is_redo, container_bin,
                 start_config, container_registry, container_user, local_build):
    '''
    Determine if a container image needs to be rebuilt, return true if so.
    '''
    
    container_dir = os.path.join(lab_path, name)
    labname = os.path.basename(lab_path)
    should_be_exec = ['rc.local', 'fixlocal.sh']
    retval = False

    #image_exists, result, dumb = ImageExists(image_name, container_registry)
    if image_info is not None and not is_redo:
        labutils.logger.debug('Container %s image %s exists, not a redo, just return (no need to check build)' % (container_name, image_name))
        return False
    elif image_info is None:
        return True 

    x=parse(image_info.creation)
    ts = calendar.timegm(x.timetuple())
    labutils.logger.debug('image ts %s  %s' % (ts, image_info.creation))
   
    ''' look at dockerfiles '''
    df_name = 'Dockerfile.%s' % container_name
    df = os.path.join(lab_path, 'dockerfiles', df_name)
    if not os.path.isfile(df):
         df = df.replace('instructor', 'student')

    ''' get ts of base image '''
    ts_base, bname = BaseImageTime(df, container_registry)
    if ts_base == 0 and local_build:
        ts_base, bname = BaseImageTime(df, None)
        
    if ts_base > ts:
        labutils.logger.warning('Base image %s changed, will build %s' % (bname, name))
        retval = True
    elif FileModLater(ts, df):
        labutils.logger.warning('dockerfile %s changed, will build %s' % (df, name))
        retval = True
    else:
        ''' look for new/deleted files in the container '''
        labutils.logger.debug('container dir %s' % container_dir)
        big_list = GetBigFiles(lab_path)
        if FileModLater(ts, container_dir, big_list=big_list):
           labutils.logger.warning('new/deleted %s is later, will build %s' % (container_dir, name))
           retval = True
        else:
            ''' look at all files/directories in container '''
                            
            flist = os.listdir(container_dir)
            for f in flist:
                check_file = None
                #if f == 'sys_tar':
                #    check_file = os.path.join(container_dir, f, 'sys.tar')
                #elif f == 'home_tar':
                #    check_file = os.path.join(container_dir, f, 'home.tar')
                #elif os.path.isdir(os.path.join(container_dir,f)):
                if os.path.isdir(os.path.join(container_dir,f)):
                    check_file = newest_file_in_tree(os.path.join(container_dir, f))
                else:
                    check_file = os.path.join(container_dir, f)
                labutils.logger.debug('check file %s' % check_file)
                if check_file in big_list:
                    labutils.logger.debug('CheckBuid ignore big file %s' % check_file)
                    continue
                if FileModLater(ts, check_file, big_list=big_list):
                    labutils.logger.warning('files in container %s is later, will build %s' % (check_file, name))
                    retval = True
                    break

    if not retval:
        param_file = os.path.join(lab_path, 'config', 'parameter.config')
        if os.path.isfile(param_file):
            if FileModLater(ts, param_file):
              labutils.logger.debug('%s is later, see if container is named' % param_file)
              with open(param_file) as param_fh:
                for line in param_fh:
                    if line.startswith('#') or ' : ' not in line:
                        continue
                    parts = line.split(' : ')
                    filenames = parts[2].split(';')
                    for fname in filenames: 
                        fname = f.strip()
                        # look for container, or lack of any container qualifier in file name
                        if fname != 'start.config':
                            if fname.startswith(container_name+':') or len(parts)<3 or ':' not in fname:
                                labutils.logger.warning('%s is later and %s mentioned in it, will build' % (param_file, container_name))
                                retval = True
                                break
                    if retval:
                        break
    if not retval:
        big_external = os.path.join(lab_path, 'config', 'bigexternal.txt')
        if os.path.isfile(big_external):
            if FileModLater(ts, big_external):
                with open(big_external) as fh:
                    for line in fh:
                        if not line.startswith('#'):
                            parts = line.split()
                            if len(parts) > 1:
                                dest = parts[1].split('/')[0]
                                if dest == container_name:
                                    retval = True
                                    labutils.logger.debug('config/bigexternal.txt is later, will rebuild')
                                    break
    
    #if not retval and container_bin is not None:
    #    all_bin_files = os.listdir(container_bin)
    #    for f in all_bin_files:
    #        if f.endswith('.swp'):
    #            continue
    #        f_path = os.path.join(container_bin, f)
    #        if FileModLater(ts, f_path):
    #           logger.warning('container_bin %s is later, will build %s' % (f_path, name))
    #           retval = True
    #           break

    if not retval and image_info.local:
        user, password = GetImageUser(image_name, container_registry)
        if user != container_user:
            labutils.logger.warning('user changed from %s to %s, will build %s' % (user, container_user, name))
            retval = True

    labutils.logger.debug('returning retval of %s' % str(retval))    
    return retval

def CheckBuildError(output, labname, name):
    fatal_error = False
    labutils.logger.debug('CheckBuildError ')
    for line in output.splitlines():
    #while output is not None: 
        #line = output.readline().decode('utf-8') 
        labutils.logger.debug('CheckBuildError x line %s' % str(line))
        if len(line) == 0:
            break 
        #line = line.decode('utf-8').strip()
        labutils.logger.debug('CheckBuildError line %s' % line)
        if len(line) > 0:
            if 'Error in docker build result' in line:
                code = line.strip().split()[-1]
                if code in ['1', '2', '9']:
                    labutils.logger.error("%s\nPlease fix Dockerfile.%s.%s.student. Look in %s for specifics on the error." % (line, 
                       labname, name, labutils.logger.file_name))
                    fatal_error = True
                else:
                    labutils.logger.debug('*** DOCKER BUILD ERROR: %s' % line)

            elif 'syntax error' in line:
                labutils.logger.error("%s\nPlease fix Dockerfile.%s.%s.student. Look in %s for specifics on the error." % (line, 
                       labname, name, labutils.logger.file_name))
                fatal_error = True
            else:
                labutils.logger.debug(line)
        else:
            break
    return fatal_error

def DoRebuildLab(lab_path, force_build=False, just_container=None, 
                 start_config=None, labtainer_config=None, run_container=None, servers=None, 
                 clone_count=None, no_pull=False, no_build=False, use_cache=True, local_build=False):
    retval = []
    labname = os.path.basename(lab_path)
    labutils.isValidLab(lab_path)
    if start_config is None:
        labtainer_config, start_config = labutils.GetBothConfigs(lab_path, labutils.logger, servers, clone_count)
    host_home_xfer = labtainer_config.host_home_xfer

    build_student = 'bin/buildImage.sh'
    LABS_DIR = os.path.abspath('../../labs')
    didfix = False
    ''' hackey assumption about running from labtainers-student or labtainers-instructor '''
    container_bin = './lab_bin'
    for name, container in start_config.containers.items():
        labutils.logger.debug('this container name %s just_container %s' % (name, just_container))
        if just_container is not None and just_container != name:
            continue
        elif just_container == name:
            force_build = True
            print('Force build of %s' % just_container)
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        if container.registry == labtainer_config.test_registry:
            branch, container_registry = registry.getBranchRegistry()
            base_registry = container_registry
        else:
            container_registry = container.registry
            base_registry = container.base_registry

        clone_names = labutils.GetContainerCloneNames(container)
        for clone_full in clone_names:
            cmd = 'docker rm %s' % clone_full
            ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = ps.communicate()
            #labutils.logger.debug("Command was (%s)" % cmd)
            if len(output[1]) > 0:
                if 'running container' in output[1].decode('utf-8'):
                    labutils.logger.debug("Error from command %s was  '%s'" % (cmd, output[1].decode('utf-8')))
                    exit(1)
                else:
                    labutils.logger.debug("non-fatal Error from command %s was  '%s'" % (cmd, output[1].decode('utf-8')))

        if container.from_image is not None:
            labutils.logger.debug('skip image taken from %s' % container.from_image)
            continue

        force_this_build = force_build
        if container.no_pull == 'YES':
            no_pull = True
        labutils.logger.debug('force_this_build: %r no_pull %r' % (force_this_build, no_pull))
        image_info = labutils.imageInfo(mycontainer_image_name, container_registry, base_registry, labtainer_config, 
                    is_rebuild=True, no_pull=no_pull, local_build=local_build)
        if not force_this_build and image_info is None:
            if not local_build:
                labutils.logger.debug('Image %s exists nowhere, so force the build' % mycontainer_image_name)
                print('Image %s exists nowhere, so force the build' % mycontainer_image_name)
            else:
                labutils.logger.debug('Image %s does not exist locally.  Local build requested, so force the build' % mycontainer_image_name)
                print('Image %s does not exist locally.  Local build requested, so force the build' % mycontainer_image_name)
                 
            force_this_build = True
        container_dir = os.path.join(lab_path, name)
        try:
            os.mkdir(os.path.join(container_dir, 'home_tar'))
        except:
            pass
        try:
            os.mkdir(os.path.join(container_dir, 'sys_tar'))
        except:
            pass
        removeStrays(container_dir, name, labname)
        ''' make sure big files have been copied before checking tars '''
        BigFiles.BigFiles(lab_path)
        BigExternal.BigExternal(lab_path, labutils.logger)
        ''' create sys_tar and home_tar before checking build dependencies '''
        CheckTars.CheckTars(container_dir, name, labutils.logger)
        if force_this_build or CheckBuild(lab_path, mycontainer_image_name, image_info, mycontainer_name, 
                                   name, True, container_bin, start_config, base_registry, container.user,
                                   local_build):

            if no_build:
                labutils.logger.debug("Would (but won't) rebuild %s" % (mycontainer_name))
                print("Would (but won't) rebuild %s" % (mycontainer_name))
                return retval
                
            labutils.logger.debug("Will rebuild %s,  force_this_build: %s  apt_source %s" % (mycontainer_name, force_this_build, labtainer_config.apt_source))
            
            #Check if the container's Dockerfile exists
            dfile = '%s/%s/dockerfiles/Dockerfile.%s.%s.student' % (LABS_DIR, labname, labname, name)
            if not os.path.isfile(dfile):
                labutils.logger.error("Dockerfile.%s.%s.student is missing from labs/%s/dockerfiles." % (labname, name, labname))
                exit(1)
            if local_build:
                ts, thebase = BaseImageTime(dfile, base_registry)
                if ts == 0:
                    labutils.logger.debug('No base found %s, look for local base' % thebase)
                    ts, thebase = BaseImageTime(dfile, None)
                    if ts == 0:
                        labutils.logger.error('No local image for %s and local build requested. Try "docker pull %s/%s"' % (thebase, base_registry, the_base))
                        exit(1)
                    else:
                        
                        labutils.logger.debug('Using local version of base %s' % thebase)
                        base_registry = 'LOCAL'
          
                else:
                    labutils.logger.debug('got ts, base %s' % thebase)

            retval.append(RegistryInfo(name, container.image_name, container_registry, base_registry))

            if os.path.isfile(build_student):
                cmd = '%s %s %s %s %s %s %s %s %s %s %s %s' % (build_student, labname, name, container.user, 
                      container.password, True, LABS_DIR, labtainer_config.apt_source, base_registry, labutils.framework_version, str(local_build), str(use_cache))
            else:
                labutils.logger.error("no image rebuild script\n")
                exit(1)
            labutils.logger.debug('cmd is %s' % cmd)     
            ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = ps.communicate()
            labutils.logger.debug('build_image back from communicate')
            #fatal_error = CheckBuildError(ps.stdout, labname, name)
            fatal_error = CheckBuildError(output[0].decode('utf-8'), labname, name)
            if not fatal_error:
                labutils.logger.debug('not fatal, do stderr')
                fatal_error = CheckBuildError(output[1].decode('utf-8'), labname, name)
                #fatal_error = CheckBuildError(ps.stderr, labname, name)
            else:
                labutils.logger.debug('fatal, do stderr')
                CheckBuildError(output[1].decode('utf-8'), labname, name)
                #CheckBuildError(ps.stderr, labname, name)
            labutils.logger.debug('done checkerror fatal %r' % fatal_error)
            if ps.returncode != 0:
                labutils.logger.error('Problem building %s, check log at $LABTAINER_DIR/logs/docker_build.log' % labname)
                exit(1)
            if fatal_error:
                exit(1)
    return retval

def RebuildLab(lab_path, force_build=False, quiet_start=False, just_container=None, 
         run_container=None, servers=None, clone_count=None, no_pull=False, use_cache=True, 
         local_build=False, just_build=False):
    # Pass 'True' to ignore_stop_error (i.e., ignore certain error encountered during StopLab
    #                                         since it might not even be an error)
    labutils.StopLab(lab_path, True, run_container=run_container, servers=servers, clone_count=clone_count)
    labutils.logger.debug('Back from StopLab clone_count was %s' % clone_count)
    labname = os.path.basename(lab_path)
    my_start_config = os.path.join('./.tmp',labname, 'start.config')
    if os.path.isfile(my_start_config):
        labutils.logger.debug('Cached start.config removed %s' % my_start_config)
        os.remove(my_start_config)
    labtainer_config, start_config = labutils.GetBothConfigs(lab_path, labutils.logger, servers, clone_count)
    
    DoRebuildLab(lab_path, force_build=force_build, 
                 just_container=just_container, start_config = start_config, 
                 labtainer_config = labtainer_config, run_container=run_container, 
                 servers=servers, clone_count=clone_count, no_pull=no_pull, use_cache=use_cache, local_build=local_build)
    if not just_build:
        # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
        host_home_xfer = labtainer_config.host_home_xfer
        myhomedir = os.environ['HOME']
        host_xfer_dir = '%s/%s' % (myhomedir, host_home_xfer)
        labutils.CreateHostHomeXfer(host_xfer_dir)
        labutils.DoStart(start_config, labtainer_config, lab_path, quiet_start, 
            run_container, servers, clone_count)
    if start_config.gns3.lower() == "yes":
        nonet = os.path.join(os.getenv('LABTAINER_DIR'), 'scripts', 'gns3', 'noNet.py')
        cmd = '%s %s' % (nonet, labname) 
        ps = subprocess.Popen(shlex.split(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1]) > 0:
            labutils.logger.error(output[1].decode('utf-8'))
        else:
            for line in output[0].decode('utf-8').splitlines():
                print(line)
        gennet = os.path.join(os.getenv('LABTAINER_DIR'), 'scripts', 'gns3', 'genNet.py')
        cmd = '%s %s %s' % (gennet, labname, labname) 
        ps = subprocess.Popen(shlex.split(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1]) > 0:
            labutils.logger.error(output[1].decode('utf-8'))
        else:
            for line in output[0].decode('utf-8').splitlines():
                print(line)

def main():
    parser = argparse.ArgumentParser(description='Build the images of a lab and start the lab.',prog='rebuild')
    parser.add_argument('labname', help='The lab to build')
    parser.add_argument('-f', '--force', action='store_true', help='Force build of all containers in the lab.')
    parser.add_argument('-p', '--prompt', action='store_true', help='prompt for email, otherwise use stored')
    parser.add_argument('-C', '--force_container', action='store', help='force rebuild just this container')
    parser.add_argument('-o', '--only_container', action='store', help='run only this container')
    parser.add_argument('-t', '--test_registry', action='store_true', default=False, help='build from images in the test registry')
    parser.add_argument('-s', '--servers', action='store_true', help='Start containers that are not clients -- intended for distributed Labtainers')
    parser.add_argument('-w', '--workstation', action='store_true', help='Intended for distributed Labtainers, start the client workstation.')
    parser.add_argument('-n', '--client_count', action='store', help='Number of clones of client containers to create, intended for multi-user labs')
    parser.add_argument('-L', '--local_build', action='store_true', default=False, help='Local building, do not pull or query from internet')
    parser.add_argument('-N', '--no_cache', action='store_true', default=False, help='Build the image without using Docker cache')
    parser.add_argument('-b', '--just_build', action='store_true', help='Only build the lab, do not start it.')


    args = parser.parse_args()
    quiet_start = True
    if args.prompt == True:
        quiet_start = False
    if args.force is not None:
        force_build = args.force
    #print('force %s quiet %s container %s' % (force_build, quiet_start, args.container))
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", args.labname, "../../config/labtainer.config")
    labutils.logger.info("Begin logging Rebuild.py for %s lab" % args.labname)
    lab_path = os.path.join(os.path.abspath('../../labs'), args.labname)

    if args.test_registry:
        if os.getenv('TEST_REGISTRY') is None:
            #print('use putenv to set it')
            os.putenv("TEST_REGISTRY", "TRUE")
            ''' why does putenv not set the value? '''
            os.environ['TEST_REGISTRY'] = 'TRUE'
        else:
            #print('exists, set it true')
            os.environ['TEST_REGISTRY'] = 'TRUE'
        print('set TEST REG to %s' % os.getenv('TEST_REGISTRY'))

    distributed = None
    if args.servers and args.workstation:
        print('--server and --workstation are mutually exclusive')
        exit(1)
    elif args.servers: 
        distributed = 'server' 
    elif args.workstation:
        distributed = 'client'
    use_cache = not args.no_cache
    RebuildLab(lab_path, force_build=force_build, quiet_start=quiet_start, 
          just_container=args.force_container, run_container=args.only_container, servers=distributed, 
          clone_count=args.client_count, local_build=args.local_build, use_cache=use_cache, just_build=args.just_build)
    current_lab = CurrentLab.CurrentLab()
    current_lab.add('lab_name', args.labname)
    current_lab.add('clone_count', args.client_count)
    current_lab.add('servers', distributed)
    current_lab.save()

    return 0

if __name__ == '__main__':
    sys.exit(main())

