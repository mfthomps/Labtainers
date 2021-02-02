#!/bin/bash
#
# Merge premaster repo and docker images into master
#   -- Performs a git merge of premaster into master
#   -- Ensures the Docker Hub matches the premaster registry
#   -- Pushes premaster and master to github
#
if [[ $1 == "-h" ]];then
    echo "Merge premaster into master, update docker hub to match mirror."
    echo "Use -n to skip docker hub update."
    exit
fi
branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$branch" != "premaster" ]]; then
    echo "Current branch is not premaster."
    exit 1
fi
git pull
git checkout master || exit 1
git merge premaster || exit 1
if [[ $1 != "-n" ]];then
    echo "Provide Docker Hub password below"
    ./refresh_mirror.py -q || exit 1
    echo "Mirror refresh complete"
fi
git push --set-upstream origin master || exit 1
git checkout premaster || exit 1
git merge master || exit 1
git push --set-upstream origin premaster || exit 1
