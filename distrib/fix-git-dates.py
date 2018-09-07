#!/usr/bin/env python

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

args = parser.parse_args()
logger.basicConfig(level=logger.DEBUG if args.verbose else logger.ERROR,
                   format='%(levelname)s:\t%(message)s')

# Find repo's top level.
try:
    workdir = os.path.abspath(subprocess.check_output(shlex.split(
                    'git rev-parse --show-toplevel')).strip())
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
    for f in filelist:
        source = os.path.join(workdir, f)
        dest = os.path.join(dist_path, f)
        if os.path.isfile(dest):
            mtime = int(os.path.getmtime(source))
            os.utime(dest, (mtime, mtime))

if args.pathspec.strip() == './':
    cmd = 'git archive master | tar -x -C %s' % (args.dist_path)
else:
    cmd = 'git archive master %s | tar -x -C %s' % (args.pathspec, args.dist_path)
os.system(cmd)

fixtimes(filelist, args.dist_path, args.pathspec, workdir)

