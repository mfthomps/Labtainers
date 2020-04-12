#!/usr/bin/env python3
'''
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
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
import glob
import os
import pwd
import shutil
import sys
import argparse
import subprocess
import time

# Filename: new_lab_setup.py
# Description:
# This is the lab setup script to be run by the lab designer.
# Please refer to the "Lab Designer User Guide" (labdesigner.pdf)
# Note:
# 1. This script checks to make sure LABTAINER_DIR is defined
#
LABTAINER_DIR=None
tdir=None

def handle_delete_container(tdir, deletecontainer):
    # This assumes directories 'config', 'dockerfiles' and 'instr_config'
    # have been properly populated
    if deletecontainer != deletecontainer.lower():
        print('Container to be deleted (%s) must be all lower case' % deletecontainer)
        sys.exit(1)
    elif ' ' in deletecontainer:
        print('Container to be deleted (%s) cannot contain spaces' % deletecontainer)
        sys.exit(1)
    here = os.getcwd()
    labname = os.path.basename(here)
    # Try to remove the container directory
    try:
        shutil.rmtree(os.path.join(here, deletecontainer))
    except Exception as e:
        print(e)
        sys.exit(1)

    # Make sure start.config exist already
    start_config_filename = 'config/start.config'
    if not os.path.exists(start_config_filename):
        print('Configuration file start.config does not exist!')
        sys.exit(1)

    # Read start.config
    start_config_file = open(start_config_filename, 'r')
    orig_start_configlines = start_config_file.readlines()
    start_config_file.close()
    # Write back start.config - minus the <deletecontainer>
    start_config_file = open(start_config_filename, 'w')
    deletecontainer_line_found = False
    for line in orig_start_configlines:
        if line.startswith('CONTAINER'):
            if deletecontainer in line:
                deletecontainer_line_found = True
            else:
                # found the next 'container' - restart copying
                # by setting deletecontainer_line_found to False
                if deletecontainer_line_found:
                    deletecontainer_line_found = False
        if not deletecontainer_line_found:
            start_config_file.write(line)
    start_config_file.close()

def copy_container(start_config_file, oldcontainer, newcontainer):
    grabbed = []
    with open(start_config_file, 'r') as fh:
        grab = False
        for line in fh:
            if not grab and line.strip().startswith('CONTAINER'): 
                cname = line.strip().split()[1]
                if cname == oldcontainer:
                    grab = True
                    cline = 'CONTAINER %s' % newcontainer
                    grabbed.append(cline)
            elif grab:
                if line.strip().startswith('CONTAINER'): 
                    grab = False
                else:
                    grabbed.append(line)
    fh = open(start_config_file, 'a')
    for line in grabbed:
        fh.write(line)
    fh.close()
    
def handle_copy_container(tdir, oldcontainer, newcontainer):
    start_config_filename = 'config/start.config'
    copy_container(start_config_filename, oldcontainer, newcontainer)
    here = os.getcwd()
    labname = os.path.basename(here)
    source_dfile = 'dockerfiles/Dockerfile.%s.%s.student' % (labname, oldcontainer)
    dest_dfile = 'dockerfiles/Dockerfile.%s.%s.student' % (labname, newcontainer)
    shutil.copyfile(source_dfile, dest_dfile)
    shutil.copytree(os.path.join('./',oldcontainer), os.path.join('./',newcontainer))
    print('** Manually adjust IP addresses for the new %s container **' % newcontainer)
        
def add_container(start_config_filename, newcontainer, basename):
    # Open start.config with append
    start_config_file = open(start_config_filename, 'a')
    start_config_file.write('CONTAINER %s\n' % newcontainer)
    start_config_file.write('\tUSER ubuntu\n')
    start_config_file.write('\tSCRIPT NONE\n')
    start_config_file.write('\tX11 YES\n')
    start_config_file.close()

def handle_add_container(tdir, newcontainer, basename='base'):
    # This assumes directories 'config', 'dockerfiles' and 'instr_config'
    # have been properly populated
    if newcontainer != newcontainer.lower():
        print('New container name is (%s)' % newcontainer)
        print('New container names must be all lower case')
        sys.exit(1)
    elif ' ' in newcontainer:
        print('New container name is (%s)' % newcontainer)
        print('New container names cannot contain spaces')
        sys.exit(1)
    template_dirs = os.listdir(tdir)
    here = os.getcwd()
    labname = os.path.basename(here)
    # Create the new container name directory
    os.mkdir(newcontainer)
    for source in template_dirs:
        if source == 'config' or source == 'instr_config' or source == 'dockerfiles':
            # This assumes directories 'config', 'dockerfiles' and 'instr_config'
            # Will add the dockerfile for the new container and modify the start.config later
            continue
        # populate new container directory with _bin and _system if they exist
        if source == '_bin' or source == '_system':
            try:
                shutil.copytree(os.path.join(tdir, source), os.path.join(here, newcontainer, source)) 
            except:
                print('error copying %s to %s, expected %s to be empty' % (source, here, here))
                sys.exit(1)

    # Make sure start.config exist already
    # then update it with the new container using start.config.template
    start_config_filename = 'config/start.config'
    if not (os.path.exists(start_config_filename) and os.path.isfile(start_config_filename)):
        print('Configuration file start.config does not exist!')
        sys.exit(1)
    add_container(start_config_filename, newcontainer, basename)

    
    # Write Dockerfile for the added container
    dfile, level0_bases = find_template(here, tdir, basename)
    if dfile == None:
        sys.exit()
    docker_template = os.path.join(tdir, 'dockerfiles', dfile)
    dockerfiles = os.path.join(here, 'dockerfiles')
    try:
        os.mkdir(dockerfiles)
    except:
        pass
    newcontainer_dockerfilename = 'Dockerfile.%s.%s.student' % (labname, newcontainer)
    write_template(docker_template, os.path.join(dockerfiles, newcontainer_dockerfilename), basename, level0_bases)

def renameSVN(old, new):
    cmd = 'git status -s %s' % old
    #print('cmd is %s' % cmd)
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    #print('out[0] %s' % output[0].decode('utf-8'))
    if output[0].decode('utf-8').strip().startswith('??'):
        os.rename(old, new)
    else:
        cmd = 'git mv %s %s' % (old, new)
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1]) > 0:
            print("Error from git mv: %s" % output[1].decode('utf-8'))
 
def handle_rename_lab(newlabname):
    here = os.getcwd()
    oldlabname = os.path.basename(here)
    currentlabpath = os.path.abspath(here)
    newlabpath = currentlabpath.replace(oldlabname, newlabname)
    if os.path.exists(newlabpath):
        print('%s already exists' % newlabpath)
        exit(1)
    shutil.move(here, newlabpath)
    # Rename dockerfiles
    newlabname_olddockerfilename = os.path.join(newlabpath, 'dockerfiles')
    newlabname_olddockerfiles = glob.glob('%s/*' % newlabname_olddockerfilename)
    for name in newlabname_olddockerfiles:
        fname = os.path.basename(name)
        # Replace only the first occurence to prevent replacing the container name portion
        newfname = fname.replace(oldlabname, newlabname, 1)
        newname = os.path.join(os.path.dirname(name), newfname)
        #print "name is (%s) newname is (%s)" % (name, newname)
        # Rename dockerfiles as new labname dockerfiles
        try:
            renameSVN(name, newname)
        except Exception as e:
            print('error renaming %s to %s %s' % (name, newname, str(e)))
            exit(1)
    count_container_lines = 0
    start_config_filename = os.path.join(newlabpath, 'config', 'start.config')
    start_config_file = open(start_config_filename, 'r')
    start_config_filelines = start_config_file.readlines()
    for line in start_config_filelines:
        if line.startswith('CONTAINER'):
            count_container_lines = count_container_lines + 1
    #print "Number of lines that starts with 'CONTAINER' is (%d)" % count_container_lines
    if count_container_lines == 0:
        print("Can't have a no container lab!")
        sys.exit(1)
    if count_container_lines == 1:
        oldcontainerpath = os.path.join(newlabpath, oldlabname)
        newcontainerpath = os.path.join(newlabpath, newlabname)
        # Move the single old container as new container as the new labname container
        renameSVN(oldcontainerpath, newcontainerpath)

        # Also rename dockerfile again (this should take care of the container name portion)
        newlabname_olddockerfilename = os.path.join(newlabpath, 'dockerfiles')
        newlabname_olddockerfiles = glob.glob('%s/*' % newlabname_olddockerfilename)
        for name in newlabname_olddockerfiles:
            newname = name.replace(oldlabname, newlabname)
            #print "name is (%s) newname is (%s)" % (name, newname)
            # Rename dockerfiles as new labname dockerfiles
            renameSVN(name, newname)

        # Read start.config, replace 'oldlabname' as 'newlabname' into start.config
        start_config_file = open(start_config_filename, 'r')
        config_filelines = start_config_file.readlines()
        start_config_file.close()
        start_config_file = open(start_config_filename, 'w')
        for line in config_filelines:
            newline = line.replace(oldlabname, newlabname)
            newline = re.sub((r"%s$" % oldlabname.strip()), newlabname, line)
            start_config_file.write(newline)

def handle_clone_lab(tdir, newlabname):
    if newlabname != newlabname.lower():
        print('New lab name is (%s)' % newlabname)
        print('New lab names must be all lower case')
        sys.exit(1)
    elif ' ' in newlabname:
        print('New lab name is (%s)' % newlabname)
        print('New lab names cannot contain spaces')
        sys.exit(1)
    here = os.getcwd()
    oldlabname = os.path.basename(here)
    currentlabpath = os.path.abspath(here)
    newlabpath = currentlabpath.replace(oldlabname, newlabname)
    #print "currentlabpath is (%s)" % currentlabpath
    #print "newlabpath is (%s)" % newlabpath

    # Make sure new lab directory does not exist
    if os.path.exists(newlabpath):
        print("New lab name already exists!")
        sys.exit(1)

    # Copy old lab as new lab
    shutil.copytree(currentlabpath, newlabpath)

    # Rename dockerfiles
    newlabname_olddockerfilename = os.path.join(newlabpath, 'dockerfiles')
    newlabname_olddockerfiles = glob.glob('%s/*' % newlabname_olddockerfilename)
    for name in newlabname_olddockerfiles:
        fname = os.path.basename(name)
        # Replace only the first occurence to prevent replacing the container name portion
        #print('fname is  %s oldlabname is %s, new is %s' % (fname, oldlabname, newlabname))
        newfname = fname.replace(oldlabname, newlabname, 1)
        newname = os.path.join(os.path.dirname(name), newfname)
        #print "name is (%s) newname is (%s)" % (name, newname)
        # Rename dockerfiles as new labname dockerfiles
        try:
            renameSVN(name, newname)
        except Exception as e:
            print('error renaming %s to %s %s' % (name, newname, str(e)))
            exit(1)

    # Handle a single container lab cloning.  Special case to rename the
    # container.  If multiple containers, we assume the container names
    # are not tied to the lab name
    count_container_lines = 0
    start_config_filename = os.path.join(newlabpath, 'config', 'start.config')
    start_config_file = open(start_config_filename, 'r')
    start_config_filelines = start_config_file.readlines()
    for line in start_config_filelines:
        if line.startswith('CONTAINER'):
            count_container_lines = count_container_lines + 1
    #print "Number of lines that starts with 'CONTAINER' is (%d)" % count_container_lines
    if count_container_lines == 0:
        print("Can't have a no container lab!")
        sys.exit(1)
    if count_container_lines == 1:
        oldcontainerpath = os.path.join(newlabpath, oldlabname)
        newcontainerpath = os.path.join(newlabpath, newlabname)
        # Move the single old container as new container as the new labname container
        renameSVN(oldcontainerpath, newcontainerpath)

        # Also rename dockerfile again (this should take care of the container name portion)
        newlabname_olddockerfilename = os.path.join(newlabpath, 'dockerfiles')
        newlabname_olddockerfiles = glob.glob('%s/*' % newlabname_olddockerfilename)
        for name in newlabname_olddockerfiles:
            # rsplit(old, new, 1)
            newname = newlabname.join(name.rsplit(oldlabname, 1))
            #print('name: %s oldlabname: %s newlabname %s  newname: %s' % (name, oldlabname, newlabname, newname))
            #print "name is (%s) newname is (%s)" % (name, newname)
            # Rename dockerfiles as new labname dockerfiles
            try:
                renameSVN(name, newname)
            except:
                print("ERROR, could not rename, name is (%s) newname is (%s)" % (name, newname))
                exit(1)

        # Read start.config, replace 'oldlabname' as 'newlabname' into start.config
        start_config_file = open(start_config_filename, 'r')
        config_filelines = start_config_file.readlines()
        start_config_file.close()
        start_config_file = open(start_config_filename, 'w')
        for line in config_filelines:
            newline = line.replace(oldlabname, newlabname)
            start_config_file.write(newline)

    # If we are cloning - fix the 'parameter.config', 'results.config' and 'goals.config'
    # i.e., use the templates configuration files instead
    parameter_config = os.path.join(newlabpath, 'config', 'parameter.config')
    results_config = os.path.join(newlabpath, 'instr_config', 'results.config')
    goals_config = os.path.join(newlabpath, 'instr_config', 'goals.config')
    template_parameter_config = os.path.join(tdir, 'config', 'parameter.config')
    template_results_config = os.path.join(tdir, 'instr_config', 'results.config')
    template_goals_config = os.path.join(tdir, 'instr_config', 'goals.config')
    os.remove(parameter_config)
    os.remove(results_config)
    os.remove(goals_config)
    shutil.copy(template_parameter_config, parameter_config)
    shutil.copy(template_results_config, results_config)
    shutil.copy(template_goals_config, goals_config)
    return oldlabname

def handle_replace_container(tdir, oldcontainer, newcontainer):
    # This assumes directories 'config', 'dockerfiles' and 'instr_config'
    # have been properly populated
    if newcontainer != newcontainer.lower():
        print('New container name is (%s)' % newcontainer)
        print('New container names must be all lower case')
        sys.exit(1)
    elif ' ' in newcontainer:
        print('New container name is (%s)' % newcontainer)
        print('New container names cannot contain spaces')
        sys.exit(1)
    here = os.getcwd()
    labname = os.path.basename(here)

    # Make sure oldcontainer directory exist
    if not (os.path.exists(oldcontainer) and os.path.isdir(oldcontainer)):
        print("Old container directory does not exists!")
        sys.exit(1)

    # Make sure newcontainer directory does not exist
    if os.path.exists(newcontainer):
        print("New container already exists!")
        sys.exit(1)

    # Make sure oldcontainer dockerfile exist
    olddockerfilename = 'Dockerfile.%s.%s.student' % (labname, oldcontainer)
    olddockerfile = os.path.join(here, 'dockerfiles', olddockerfilename)
    if not (os.path.exists(olddockerfile) and os.path.isfile(olddockerfile)):
        print("Old container dockerfile does not exists!")
        sys.exit(1)

    # Make sure newcontainer dockerfile does not exist
    newdockerfilename = 'Dockerfile.%s.%s.student' % (labname, newcontainer)
    newdockerfile = os.path.join(here, 'dockerfiles', newdockerfilename)
    if os.path.exists(newdockerfile):
        print("New container dockerfile already exists!")
        sys.exit(1)

    # Make sure start.config exist already
    start_config_filename = 'config/start.config'
    # then update it with the new container using start.config.template
    if not (os.path.exists(start_config_filename) and os.path.isfile(start_config_filename)):
        print('Configuration file start.config does not exist!')
        sys.exit(1)

    # Rename oldcontainer as newcontainer
    renameSVN(oldcontainer, newcontainer)

    # Rename oldcontainer dockerfile as newcontainer dockerfile
    renameSVN(olddockerfile, newdockerfile)
    
    # Read start.config, replace 'oldcontainer' as 'newcontainer' into start.config
    start_config_file = open(start_config_filename, 'r')
    config_filelines = start_config_file.readlines()
    start_config_file.close()
    start_config_file = open(start_config_filename, 'w')
    for line in config_filelines:
        if 'LAB_MASTER_SEED' not in line:
            newline = line.replace(oldcontainer, newcontainer)
        else:
            newline = line
        start_config_file.write(newline)
    start_config_file.close()

def find_template(here, tdir, basename):
    ##Store the current working directory to restore later
    new_lab_dir = os.getcwd()
    
    ##Change working directory to the directory of base dockerfiles
    os.chdir("../../scripts/designer/base_dockerfiles")

    ##Get list of files and clean it up to only include 'Dockerfile.labtainer.' files
    base_dockerfiles = glob.glob("Dockerfile.labtainer.*")
    #print(base_dockerfiles)

   
    ##Make list of potential level 0 bases (bases that will have specific template files to them)
    level0_bases = []
    base_dockerfiles_tmp = list(base_dockerfiles)
    for base_dfile in base_dockerfiles:
        not_base0 = False

        open_dfile = open(base_dfile)
        line = open_dfile.readline()
        while line:
            if line.startswith('FROM $registry/labtainer.') or line.startswith('FROM mfthomps/labtainer.'):
                not_base0 = True
                break
            line = open_dfile.readline()
        open_dfile.close()

        if not not_base0:
            #print('Base0:' + base_dfile)
            level0_bases.append(base_dfile)
            base_dockerfiles_tmp.remove(base_dfile)

    base_dockerfiles = list(base_dockerfiles_tmp)
    #print(base_dockerfiles) 

    ##Make map of bases
    bases_map = dict((base,[]) for base in level0_bases)
    #print(bases_map.keys())
    while len(base_dockerfiles_tmp) != 0:
        for base_dfile in base_dockerfiles:
            open_dfile = open(base_dfile)
            line = open_dfile.readline()
            while line:
                if line.startswith('FROM $registry/labtainer.') or line.startswith('FROM mfthomps/labtainer.'):
                    referenced_base = "Dockerfile.labtainer.%s" % line.split('labtainer.')[1].rstrip()
                    #print("Ref Base: " + referenced_base)

                    #check if the referenced_base is a zero base
                    if referenced_base in bases_map.keys():
                        bases_map[referenced_base].append(base_dfile)
                        base_dockerfiles_tmp.remove(base_dfile)
                        break
                    #check if the referenced_base is under a zero base
                    for base0 in bases_map.keys():
                        for base in bases_map[base0]:
                            if(referenced_base == base):
                                bases_map[base0].append(base_dfile)
                                base_dockerfiles_tmp.remove(base_dfile)
                                break
                        else:
                            continue
                        break

                    #If the referenced_base is neither a zero base or under a zero base, then skip it.
                    #The next iteration through the shortened list of base_dockerfiles may find its root zero base.
                    break
                line = open_dfile.readline()
            open_dfile.close()

        if len(base_dockerfiles_tmp) > 0:
            base_dockerfiles = list(base_dockerfiles_tmp)
    #print(bases_map)

    ##Check which level 0 base the requested base uses, in other words, what dockerfile template the base will use.
    requested_dockerfile = "Dockerfile.labtainer.%s" % basename
    #print("requested base: " + requested_dockerfile)
    requested_template = ''

    #check if the requested dockerfile is a zero base
    if requested_dockerfile in bases_map.keys():
        requested_template = "Dockerfile.template.%s.student" % basename
    else:
        #check if the requested dockerfile is under a zero base
        for base0 in bases_map.keys():
            for base in bases_map[base0]:
                if(requested_dockerfile == base):
                    requested_template = "Dockerfile.template.%s.student" % base0.split('labtainer.')[1]
                    break
            else:
                continue
            break

    #If did not find requested dockerfile as zero base or under a zero base then report that it does not exists.
    if requested_template == '':
        print("ERROR Dockerfile: " + requested_dockerfile + " does not exist.")
        print('Here are the valid bases: ')
        basenames = get_listofbases(os.getcwd())
        i = 1
        for basename in basenames:
            print(str(i) + ': ' + basename)
            i = i+1
        return None, level0_bases
        #DEV NOTE: If program halts, the new lab dir needs to be reset(made empty) so there is no conlict with repopulating
        # the lab files in this dir upon runnning new_lab_setup.py again.
    
    #print("Requested docker template: " + requested_template)

    ##Check if the requested template exists
    os.chdir("../templates/dockerfiles")
    if(os.path.isfile(requested_template)):
        os.chdir(new_lab_dir)
        return requested_template, level0_bases
    else:
        print("ERROR Template: " + requested_template + " does not exist.")
        os.chdir(new_lab_dir)
        return None, level0_bases


def write_template(src, dest, basename, level0_bases):
    requested_base = 'Dockerfile.labtainer.%s' % basename
    level0_base = requested_base in level0_bases
    found_from = False
    with open(src, 'r') as src_template, open(dest, 'w') as dest_template:
        lines = src_template.readlines()
        for i, line in enumerate(lines):
            if level0_base is False and found_from is False and line.startswith('FROM $registry/labtainer.'):
                lines[i] = 'FROM $registry/labtainer.%s\n' % basename
                found_from = True

        dest_template.write("".join(lines)) 

def get_listofbases(dockerfiles_path):
    base_dockerfiles = glob.glob("Dockerfile.labtainer.*")
    
    basenames = []
    for dockerfile in base_dockerfiles:
        # As of 9/9/19: master and centos6 has no template file for to use. 
        if dockerfile != "Dockerfile.labtainer.master" and dockerfile != "Dockerfile.labtainer.centos6":
            basenames.append(dockerfile.replace("Dockerfile.labtainer.", ""))
    return basenames


def copy_from_template(tdir, basename):
    '''
    Copy a set of initial lab configuration files into a new lab and
    adjust their names and content to reflect the lab name.
    '''
    template_dirs = os.listdir(tdir)
    here = os.getcwd()
    labname = os.path.basename(here)
    config_dir = None
    os.mkdir(labname)
    for source in template_dirs:
        if source == '_bin' or source == '_system':
            try:
                shutil.copytree(os.path.join(tdir, source), os.path.join(here, labname, source)) 
            except:
                print('error copying %s to %s, expected %s to be empty' % (source, here, here))
                exit(1)
        elif source == 'dockerfiles':
                dfile, level0_bases = find_template(here, tdir, basename)
                if dfile == None:
                    sys.exit()
                docker_template = os.path.join(tdir, 'dockerfiles', dfile)
                dockerfiles = os.path.join(here, 'dockerfiles')
                try:
                    os.mkdir(dockerfiles)
                except:
                    pass
                write_template(docker_template, os.path.join(dockerfiles, 'Dockerfile.template.template.student'), basename, level0_bases)

        else:        
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
    add_container(start_config_file, labname, basename)

def check_valid_lab(current_dir):
    is_valid = True
    labname = os.path.basename(current_dir)
    if labname != labname.lower():
        print('Lab name is (%s)' % labname)
        print('Lab names must be all lower case')
        is_valid = False
    elif ' ' in labname:
        print('Lab name is (%s)' % labname)
        print('Lab names cannot contain spaces')
        is_valid = False
    # Valid lab directory will have at least the 'config', 'dockerfiles' and 'instr_config' directories
    config_dir = os.path.join(current_dir, "config")
    dockerfiles_dir = os.path.join(current_dir, "dockerfiles")
    instr_config_dir = os.path.join(current_dir, "instr_config")
    missing_config_dir = False
    if not (os.path.exists(config_dir) and os.path.isdir(config_dir)):
        missing_config_dir = True
    missing_dockerfiles_dir = False
    if not (os.path.exists(dockerfiles_dir) and os.path.isdir(dockerfiles_dir)):
        missing_dockerfiles_dir = True
    missing_instr_config_dir = False
    if not (os.path.exists(instr_config_dir) and os.path.isdir(instr_config_dir)):
        missing_instr_config_dir = True

    # If all three directories (config, dockerfiles and instr_config) are missing
    # then DO NOT print the missing directory message
    # (lab designer must be trying to create a brand new lab)
    if (missing_config_dir and missing_dockerfiles_dir and missing_instr_config_dir):
        # Still set is_valid to False
        is_valid = False
    else:
        # Half-baked lab directory? Print the missing config files
        if missing_config_dir:
            #print("config_dir is (%s)" % config_dir)
            print("Missing config directory for labname %s" % labname)
            is_valid = False
        if missing_dockerfiles_dir:
            #print("dockerfiles_dir is (%s)" % dockerfiles_dir)
            print("Missing dockerfiles directory for labname %s" % labname)
            is_valid = False
        if missing_instr_config_dir:
            #print("instr_config_dir is (%s)" % instr_config_dir)
            print("Missing instr_config directory for labname %s" % labname)
            is_valid = False
    return is_valid

def main():
    try:
        LABTAINER_DIR = os.environ['LABTAINER_DIR']
    except:
        sys.stderr.write('LABTAINER_DIR environment variable not set.\n')
        sys.exit(1)
    tdir = os.path.join(LABTAINER_DIR, 'scripts','designer','templates')
    parser = argparse.ArgumentParser(description='Create a new lab or change an existing lab.  If no arguments are given, create a new lab in the current directory. ')
    #parser.add_argument('basename', default='NONE', nargs='?', action='store', help='What base dockerfile this ') 
    parser.add_argument('-c', '--clone_container', action='store', help='Clone the current lab to a new lab', metavar='')
    parser.add_argument('-a', '--add_container', action='store', help='Add a container to this lab', metavar='')
    parser.add_argument('-A', '--copy_container', action='store', nargs = 2, help='Add a container to this lab copied from an existing container.', metavar='')
    parser.add_argument('-r', '--rename_container', action='store', nargs = 2, help='Rename container in the lab, e.g., "-r old new"', metavar='')
    parser.add_argument('-m', '--rename_lab', action='store',  help='Rename the current lab to the given name. Warning: may break subversion!"', metavar='')
    parser.add_argument('-d', '--delete_container', action='store', help='Delete a container from this lab', metavar='')
    parser.add_argument('-b', '--base_name', action='store', help='Identify labtainer base dockerfile to be used for a new container/lab.', 
                          metavar='', default=None)

    args = parser.parse_args()

    num_arg = len(sys.argv)
    #print("LABTAINER_DIR is (%s)" % LABTAINER_DIR)
    #print("tdir is (%s)" % tdir)
    #print("number of arguments is (%d)" % num_arg)

    current_dir = os.getcwd()
    parent_dir = os.path.basename(os.path.dirname(current_dir))
    if parent_dir != "labs":
        sys.stderr.write('Lab directories must be below the labs parent directory.\n')
        sys.exit(1)

    if args.base_name is None:
        base_name = 'base'
    else:
        base_name = args.base_name
    is_valid = check_valid_lab(current_dir)
    if num_arg == 1 or (num_arg == 3 and args.base_name is not None):
        if is_valid:
            print("This already appears to be a lab directory!\n")
            parser.print_help()
        else:
            copy_from_template(tdir, base_name)
            print('New lab created.  Use "new_lab_setup.py -h" to see')
            print('options for adding components to the lab.')
    else:
        if args.add_container is not None:
            newcontainer = args.add_container
            handle_add_container(tdir, newcontainer, base_name)
            print("Added new container %s." % newcontainer)
        elif args.copy_container is not None:
            handle_copy_container(tdir, args.copy_container[0], args.copy_container[1])
            print("Container %s copied to %s." % (args.copy_container[0], args.copy_container[1]))
        elif args.clone_container is not None:
            oldlabname = handle_clone_lab(tdir, args.clone_container)
            print("Lab %s cloned to new lab %s." % (oldlabname, args.clone_container))
        elif args.delete_container is not None:
            handle_delete_container(tdir, args.delete_container)
            print("Container %s deleted." % args.delete_container)
        elif args.rename_container is not None:
            handle_replace_container(tdir, args.rename_container[0], args.rename_container[1])
            print("Container %s renamed to %s." % (args.rename_container[0], args.rename_container[1]))
        elif args.rename_lab is not None:
            was = os.path.basename(os.getcwd())
            handle_rename_lab(args.rename_lab)
            print("Container %s renamed to %s." % (was, args.rename_lab))
            print('PLEASE  cd ../%s' % args.rename_lab)
        else:
            print('Did not handle request.')
            parser.print_help()

    return 0

if __name__ == '__main__':
    sys.exit(main())


