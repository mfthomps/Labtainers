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
import subprocess, shlex
import sys, os.path
import logging as logger
import argparse
import time

parser = argparse.ArgumentParser(
    description='Use git archive and file times from the current repo to'
                'checkout a subset of a git repo with file dates taken from the'
                'repo.'
                'Current directory must be inside work tree')

parser.add_argument('--verbose', '-v',
                    action="store_true",
                    help='print warnings and debug info for each processed file. ')

parser.add_argument('pathspec',
                    help='path to subdirectory, relative to repo top')

parser.add_argument('dist_path', help='directory of distribution tree')

parser.add_argument('branch', help='branch of the repo')

args = parser.parse_args()
logger.basicConfig(level=logger.DEBUG if args.verbose else logger.ERROR,
                   format='%(levelname)s:\t%(message)s')

# Find repo's top level.
try:
    workdir = os.path.abspath(subprocess.check_output(shlex.split(
                    'git rev-parse --show-toplevel')).strip()).decode('utf-8')
except subprocess.CalledProcessError as e:
    sys.exit(e.returncode)


# List files matching user pathspec, relative to current directory
# git commands always print paths relative to work tree root
filelist = set()

path = os.path.join(workdir, args.pathspec)
# file or symlink (to file, to dir or broken - git handles the same way)
if os.path.isfile(path) or os.path.islink(path):
    filelist.add(os.path.relpath(path, workdir))

# dir
elif os.path.isdir(path):
    for root, subdirs, files in os.walk(path):
        if '.git' in subdirs:
            subdirs.remove('.git')

        for file in files:
            filelist.add(os.path.relpath(os.path.join(root, file), workdir))


def fixtimes(filelist, dist_path, pathspec, workdir):
    #print('fix times')
    for f in filelist:
        source = os.path.join(workdir, f)
        dest = os.path.join(dist_path, f)
        if os.path.isfile(dest):
            mtime = int(os.path.getmtime(source))
            os.utime(dest, (mtime, mtime))

if args.pathspec.strip() == './':
    cmd = 'git archive %s | tar -x -C %s' % (args.branch, args.dist_path)
else:
    cmd = 'git archive %s %s | tar -x -C %s' % (args.branch, args.pathspec, args.dist_path)
os.system(cmd)

fixtimes(filelist, args.dist_path, args.pathspec, workdir)

