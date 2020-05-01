#!/bin/bash
#
# Creates a new distribution.
#   -- Ensures the Docker Hub matches the premaster registry
#   -- Performs a git merge
#   -- Creates student and designer distribution from master
#   -- Pushes premaster and master to github
#
branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$branch" != "premaster" ]]; then
    echo "Current branch is not premaster."
    exit 1
fi
git pull
git checkout master || exit 1
git merge premaster || exit 1
./mkall.sh -q || exit 1
echo "Provide Docker Hub password below"
./refresh_mirror.py -q || exit 1
echo "Mirror refresh complete"
git push --set-upstream origin master || exit 1
git checkout premaster || exit 1
git push --set-upstream origin premaster || exit 1
