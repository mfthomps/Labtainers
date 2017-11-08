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
import glob
import os
import pwd
import shutil
import sys

# Filename: new_lab_setup.py
# Description:
# This is the lab setup script to be run by the lab designer.
# Please refer to the "Lab Designer User Guide" (labdesigner.pdf)
# Note:
# 1. This script checks to make sure LABTAINER_DIR is defined
#
LABTAINER_DIR=None
tdir=None

def handle_add_container(tdir, newcontainer):
    # This assumes directories 'config', 'dockerfiles' and 'instr_config'
    # have been properly populated
    print("Handle -a %s" % newcontainer)
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

    print('start.config exists!')
    # Open start.config with append
    start_config_file = open(start_config_filename, 'a')
    config_template_file = os.path.join(tdir, 'config', 'start.config.template')
    container_default_line_found = False
    default_string = 'default'
    with open(config_template_file) as fh:
        config_template_filelines = fh.readlines()
    for line in config_template_filelines:
        if line.startswith('CONTAINER'):
            container_default_line_found = True
        if container_default_line_found:
            new_line = line.replace(default_string, newcontainer)
            start_config_file.write(new_line)
    start_config_file.close()

    # Now copy dockerfiles/Dockerfile.template.template.student as
    #          dockerfiles/Dockerfile.<labname>.<newcontainer>.student
    dockerfile_template = os.path.join(tdir, 'dockerfiles', 'Dockerfile.template.template.student')
    newcontainer_dockerfilename = 'Dockerfile.%s.%s.student' % (labname, newcontainer)
    newcontainer_dockerfile = os.path.join(here, 'dockerfiles', newcontainer_dockerfilename)
    shutil.copy(dockerfile_template, newcontainer_dockerfile)

def handle_clone_lab(tdir, newlabname):
    #print("Handle -c %s" % newlabname)
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
        print "New lab name already exists!"
        sys.exit(1)

    # Copy old lab as new lab
    shutil.copytree(currentlabpath, newlabpath)

    # Rename dockerfiles
    newlabname_olddockerfilename = os.path.join(newlabpath, 'dockerfiles')
    newlabname_olddockerfiles = glob.glob('%s/*' % newlabname_olddockerfilename)
    for name in newlabname_olddockerfiles:
        # Replace only the first occurence to prevent replacing the container name portion
        newname = name.replace(oldlabname, newlabname, 1)
        #print "name is (%s) newname is (%s)" % (name, newname)
        # Rename dockerfiles as new labname dockerfiles
        os.rename(name, newname)

def handle_replace_container(tdir, oldcontainer, newcontainer):
    # This assumes directories 'config', 'dockerfiles' and 'instr_config'
    # have been properly populated
    print("Handle -r %s %s" % (oldcontainer, newcontainer))
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
        print "Old container directory does not exists!"
        sys.exit(1)

    # Make sure newcontainer directory does not exist
    if os.path.exists(newcontainer):
        print "New container already exists!"
        sys.exit(1)

    # Make sure oldcontainer dockerfile exist
    olddockerfilename = 'Dockerfile.%s.%s.student' % (labname, oldcontainer)
    olddockerfile = os.path.join(here, 'dockerfiles', olddockerfilename)
    if not (os.path.exists(olddockerfile) and os.path.isfile(olddockerfile)):
        print "Old container dockerfile does not exists!"
        sys.exit(1)

    # Make sure newcontainer dockerfile does not exist
    newdockerfilename = 'Dockerfile.%s.%s.student' % (labname, newcontainer)
    newdockerfile = os.path.join(here, 'dockerfiles', newdockerfilename)
    if os.path.exists(newdockerfile):
        print "New container dockerfile already exists!"
        sys.exit(1)

    # Make sure start.config exist already
    start_config_filename = 'config/start.config'
    # then update it with the new container using start.config.template
    if not (os.path.exists(start_config_filename) and os.path.isfile(start_config_filename)):
        print('Configuration file start.config does not exist!')
        sys.exit(1)

    # Rename oldcontainer as newcontainer
    os.rename(oldcontainer, newcontainer)

    # Rename oldcontainer dockerfile as newcontainer dockerfile
    os.rename(olddockerfile, newdockerfile)
    
    # Read start.config, replace 'oldcontainer' as 'newcontainer' into start.config
    start_config_file = open(start_config_filename, 'r')
    config_filelines = start_config_file.readlines()
    start_config_file.close()
    start_config_file = open(start_config_filename, 'w')
    for line in config_filelines:
        newline = line.replace(oldcontainer, newcontainer)
        start_config_file.write(newline)
    start_config_file.close()


def copy_from_template(tdir):
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
        else:        
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

def usage():
    sys.stderr.write("Usage: new_lab_setup.py [ -h | -a <container> | -r <oldcontainer> <newcontainer> | -c <newlabname> ]\n")
    sys.stderr.write("Arguments:\n")
    sys.stderr.write("   -h : Display usage\n")
    sys.stderr.write("   -a <container> : add a new container to the existing lab\n")
    sys.stderr.write("                    (Must be run from existing lab directory)\n")
    sys.stderr.write("   -r <oldcontainer> <newcontainer> : change a container name and update as necessary\n")
    sys.stderr.write("   -c <newlabname> : clone the current lab into a new lab with the given name\n")
    sys.stderr.write("   No arguments : do the following:\n")
    sys.stderr.write("                  1. check as a valid lab directory\n")
    sys.stderr.write("                  1.a. If it is already a valid lab directory, print that message and usage\n")
    sys.stderr.write("                  1.b. If it is not (i.e., empty), then copy from template\n")
    sys.exit(1)


# Usage: new_lab_setup.py [ -h | -a <container> | -r <oldcontainer> <newcontainer> | -c <newlabname> ]
# Arguments:
#    -h : Display usage
#    -a <container> : add a new container to the existing lab
#                     (Must be run from existing lab directory)
#    -c <newlabname> : clone the current lab into a new lab with the given name
#    -r <oldcontainer> <newcontainer> : change a container name and update as necessary
#    No arguments : do the following:
#                   1. check as a valid lab directory
#                   1.a. If it is already a valid lab directory, print that message and usage
#                   1.b. If it is not (i.e., empty), then copy from template
def main():
    try:
        LABTAINER_DIR = os.environ['LABTAINER_DIR']
    except:
        sys.stderr.write('LABTAINER_DIR environment variable not set.\n')
        sys.exit(1)
    tdir = os.path.join(LABTAINER_DIR, 'scripts','designer','templates')

    num_arg = len(sys.argv)
    #print("LABTAINER_DIR is (%s)" % LABTAINER_DIR)
    #print("tdir is (%s)" % tdir)
    #print("number of arguments is (%d)" % num_arg)

    current_dir = os.getcwd()
    is_valid = check_valid_lab(current_dir)
    if num_arg == 1:
        if is_valid:
            print("This already appears to be a lab directory!\n")
            usage()
        else:
            copy_from_template(tdir)
    elif num_arg == 2:
        help_option = sys.argv[1]
        #print("help_option is (%s)" % help_option)
        # Display usage regardless of what the argument is
        usage()
    elif num_arg == 3:
        option = sys.argv[1]
        if is_valid and option == "-a":
            #print("Handle -a <container>")
            newcontainer = sys.argv[2]
            handle_add_container(tdir, newcontainer)
        elif is_valid and option == "-c":
            #print("Handle -c <newlabname>")
            newlabname = sys.argv[2]
            handle_clone_lab(tdir, newlabname)
        else:
            usage()
    elif num_arg == 4:
        option = sys.argv[1]
        if is_valid and option == "-r":
            #print("Handle -r <oldcontainer> <newcontainer>")
            oldcontainer = sys.argv[2]
            newcontainer = sys.argv[3]
            handle_replace_container(tdir, oldcontainer, newcontainer)
        else:
            usage()
    else:
        usage()

    return 0

if __name__ == '__main__':
    sys.exit(main())


