#!/bin/bash
#
# Creates a new distribution.
#   -- Ensures the Docker Hub matches the premaster registry
#   -- Performs a git merge
#   -- Creates student and designer distribution from master
#   -- Pushes premaster and master to github
#
git checkout master || exit 1
git merge premaster || exit 1
./mkall.sh -q || exit 1
./refresh_mirror.py -q || exit 1
git push --set-upstream origin master || exit 1
git checkout premaster || exit 1
git push --set-upstream origin premaster || exit 1
