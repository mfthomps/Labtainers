#!/usr/bin/env python
'''
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
'''
import sys
import os
import shutil
'''
Look at _tar directories for the given labs/[lab]/[image] and
create or update tar files to reflect recent changes.  Uses
an 'external-manifest' file to identify tars from other labs
that should be part of this one.
'''
external = 'external-manifest'
tmp_loc = '/tmp/check_tar'
def expandManifest(full, tar_name):
    #print('expand for %s' % full)
    mf = os.path.join(full, external)
    labdir = os.path.dirname(os.path.dirname(os.path.dirname(full)))
    #print('labdir is %s' % labdir)
    with open(mf) as fh:
        for line in fh:
            lab, image = line.strip().split(':')
            ref_tar = os.path.join(labdir, lab, image, os.path.basename(full), tar_name)
            #print('external ref is %s' % ref_tar)
            cmd = 'tar xf %s -C %s' % (ref_tar, tmp_loc)
            os.system(cmd)

def newest_file_in_tree(rootfolder):
    return max(
        (os.path.join(dirname, filename)
        for dirname, dirnames, filenames in os.walk(rootfolder)
        for filename in filenames),
        key=lambda fn: os.stat(fn).st_mtime)

lab_dir = sys.argv[1]
image_name = sys.argv[2]
tar_list = os.listdir(lab_dir)
manifest_name = '%s-home_tar.list' % image_name
manifest = os.path.join(os.path.dirname(lab_dir), 'config', manifest_name)
try:
    shutil.rmtree(tmp_loc)
except:
    pass
os.mkdir(tmp_loc)
for f in tar_list:
    full = os.path.join(lab_dir, f)
    if os.path.isdir(full) and f.endswith('_tar'):
        os.chdir(full)
        tmp_name = f[:-4]
        tar_name = tmp_name+'.tar'
        #print('check for %s' % tar_name)
        if not os.path.isfile(tar_name):
            ''' no tar, make one '''
            #print('no tar %s, make one' % tar_name)
            f_list = os.listdir('./')
            if len(f_list) == 0:
                #print('no files, make empty')
                ''' no files at all, create empty archive '''
                cmd = 'tar cvf %s --files-from /dev/null' % tar_name
                os.system(cmd)
                #print('did %s' % cmd)
            else:
                if external in f_list:
                    ''' external manifest, expand that '''
                    expandManifest(full, tar_name)
                for cfile in f_list:
                    if cfile != external:
                        shutil.copytree(cfile, tmp_loc)
                os.chdir(tmp_loc)
                full_tar = os.path.join(full, tar_name)
                if f == 'home_tar':
                    cmd = 'tar czf %s `ls -A -1` > %s' % (full_tar, manifest)
                else:
                    cmd = 'tar czf %s `ls -A -1`' % (full_tar)
                os.system(cmd)
                #print('did %s' % cmd)
        else:
            ''' is a tar file, should it be updated? '''
            os.chdir(full)
            newest = newest_file_in_tree('./') 
            #print('newest is %s' % newest)
            if not newest.endswith(tar_name):
                os.remove(tar_name)
                ''' something is newer, need to update tar '''
                if os.path.isfile(os.path.join('./', external)):
                    expandManifest(full, tar_name)
                os.chdir(tmp_loc)
                full_tar = os.path.join(full, tar_name)
                if f == 'home_tar':
                    cmd = 'tar czf %s `ls -A -1` > %s' % (full_tar, manifest)
                else:
                    cmd = 'tar czf %s `ls -A -1`' % (full_tar)
                os.system(cmd)
                #print('did %s' % cmd)
            else:
                ''' tar file is the most recent.  ensure we have a manifest '''
                if not os.path.isfile(manifest):
                    os.chdir(full)
                    cmd =  'tar tf %s > %s' % (tar_file, manifest) 
                 
                
