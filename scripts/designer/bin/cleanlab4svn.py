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
import sys
import tarfile

# Filename: cleanlab4svn.py
# Description:
# This is the lab setup script to be run by the lab designer.
# This script must be run from a lab directory.
# This script will remove the following:
# 1. Any tarball '*.tar.gz' in the lab directory, i.e., <lab>/*.tar.gz files
# 2. Any tar list file, i.e., <lab>/config/*_tar.list files
# 3. Any empty tar file, i.e., <lab>/<containers>/*tar/*.tar files
# 4. Any pdf file in docs directory, i.e., <lab>/docs/*.pdf files
# Note:
# 1. This script checks to make sure LABTAINER_DIR is defined
#
LABTAINER_DIR=None

def DoWork(current_dir, lab_name):
    # This script will remove the following:
    # 1. Any tarball '*.tar.gz' in the lab directory, i.e., <lab>/*.tar.gz files
    tarball_list = glob.glob('%s/*/*.tar.gz' % current_dir)
    #print "tarball_list is (%s)" % tarball_list
    for name in tarball_list:
        #print "current name is %s" % name
        try:
            os.remove(name)
        except:
            print("Fails to remove tarball (%s)" % name)
            sys.exit(1)

    # 2. Any tar list file, i.e., <lab>/config/*_tar.list files
    tarlist_list = glob.glob('%s/config/*_tar.list' % current_dir)
    #print "tarlist_list is (%s)" % tarlist_list
    for name in tarlist_list:
        #print "current name is %s" % name
        try:
            os.remove(name)
        except:
            print("Fails to remove tar list file (%s)" % name)
            sys.exit(1)

    # 3. Any empty tar file, i.e., <lab>/<containers>/*tar/*.tar files
    tarfile_list = glob.glob('%s/*/*tar/*.tar' % current_dir)
    #print "tarfile_list is (%s)" % tarfile_list
    for name in tarfile_list:
        external_manifest_file = os.path.join(os.path.dirname(name), "external-manifest")
        #print "External manifest file is (%s)" % external_manifest_file
        # If "external-manifest" file exist, just remove the tar file
        if os.path.exists(external_manifest_file):
            try:
                os.remove(name)
            except:
                print("File external-manifest exists, but fails to remove tar file (%s)" % name)
                sys.exit(1)
            continue
        #print "current name is %s" % name
        if not os.path.isfile(name):
            print("File (%s) has tar but is not a file" % name)
            sys.exit(1)
        with tarfile.open(name) as archive:
            count = sum(1 for member in archive if member.isreg())
        if count == 0:
            try:
                os.remove(name)
            except:
                print("Fails to remove tar file (%s)" % name)
                sys.exit(1)

    # 4. Any pdf file in docs directory, i.e., <lab>/docs/*.pdf files that starts
    #    with the labname
    #print "pdflist is (%s)" % pdflist
    pdf_extensions = ['pdf','dvi','out','log','aux']
    for ext in pdf_extensions:
        pdflist = glob.glob('%s/docs/*.%s' % (current_dir, ext))
        for name in pdflist:
            #print "current name is %s" % name
            if os.path.basename(name).startswith(lab_name):
                try:
                    os.remove(name)
                except:
                    print("Fails to remove PDF file (%s)" % name)
                    sys.exit(1)
    # external big files in config/bigexternal.txt
    gitIgnoreBig(current_dir)

def check_valid_lab(current_dir):
    parent_dir = os.path.basename(os.path.dirname(current_dir))
    if parent_dir != "labs":
        sys.stderr.write('Lab directories must be below the labs parent directory.\n')
        sys.exit(1)
    labname = os.path.basename(current_dir)
    if labname != labname.lower():
        print('Lab name is (%s)' % labname)
        print('Lab names must be all lower case')
        sys.exit(1)
    elif ' ' in labname:
        print('Lab name is (%s)' % labname)
        print('Lab names cannot contain spaces')
        sys.exit(1)
    config_dir = os.path.join(current_dir, "config")
    if not (os.path.exists(config_dir) and os.path.isdir(config_dir)):
        print('Missing config directory')
        sys.exit(1)
    return labname

def gitIgnoreBig(current_dir):
    if os.path.isfile('config/bigexternal.txt'):
        ''' skip files already in gitignore '''
        ignore_list = []
        if os.path.isfile('.gitignore'):
            with open('.gitignore') as fh:
                for line in fh:
                    if line.strip().startswith('#') or len(line.strip())==0:
                        continue
                    ignore_list.append(line.strip())
                  
        gi = git_ignore = open('.gitignore', 'a')
        with open('config/bigexternal.txt') as fh:
            for line in fh:
                if line.strip().startswith('#') or len(line.strip())==0:
                    continue
                parts = line.split()
                target = parts[1].strip()
                if target not in ignore_list:
                    gi.write(target+'\n')
        gi.close()
                

def usage():
    sys.stderr.write("Usage: cleanlab4svn.py [ -h ]\n")
    sys.stderr.write("   -h : Display usage\n")
    sys.stderr.write("This script must be run from a lab directory.\n")
    sys.stderr.write("This script will remove the following:\n")
    sys.stderr.write("1. Any tarball '*.tar.gz' in the lab directory, i.e., <lab>/*.tar.gz files\n")
    sys.stderr.write("2. Any tar list file, i.e., <lab>/config/*_tar.list files\n")
    sys.stderr.write("3. Any empty tar file, i.e., <lab>/<containers>/*tar/*.tar files\n")
    sys.stderr.write("** The gitignore file will be updated to reflect files in bigexternal.txt\n")
    sys.exit(1)

# Usage: cleanlab4svn.py [ -h ]
# Arguments:
#    -h : Display usage
def main():
    try:
        LABTAINER_DIR = os.environ['LABTAINER_DIR']
    except:
        sys.stderr.write('LABTAINER_DIR environment variable not set.\n')
        sys.exit(1)

    num_arg = len(sys.argv)
    #print("LABTAINER_DIR is (%s)" % LABTAINER_DIR)
    #print("number of arguments is (%d)" % num_arg)

    current_dir = os.getcwd()
    lab_name = check_valid_lab(current_dir)
    if num_arg == 1:
        DoWork(current_dir, lab_name)
    else:
        # Display usage regardless of what the argument is
        usage()

    return 0

if __name__ == '__main__':
    sys.exit(main())


