#!/bin/bash
branch=$(git rev-parse --abbrev-ref HEAD)
git checkout master
git push -d origin premaster
git branch -D premaster
git checkout -b premaster
git checkout $branch
#
# echo now refresh the mirror (premaster registry) to match GitHub
#
./refresh_mirror.py -r
