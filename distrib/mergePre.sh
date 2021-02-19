#!/bin/bash
#
# Merge a branch repo and docker images into master
#   -- Performs a git merge of the branch into master
#   -- If the branch is premaster and $2 is not -n:
#       -- Ensures the Docker Hub matches the premaster registry
#   -- Pushes branch and master to github
#
branch=$1
shift 1
if [[ $1 == "-h" ]];then
    echo "Merge premaster into master, update docker hub to match mirror."
    echo "Use -n to skip docker hub update."
    exit 1
fi
cur_branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$cur_branch" != "$branch" ]]; then
    echo "Current branch is not $branch."
    exit 1
fi
git pull
git checkout master || exit 1
git merge $branch || exit 1
if [[ "$branch" == premaster ]] && [[ $1 != "-n" ]];then
    echo "Refresh docker hub with premaster images"
    echo "Provide Docker Hub password below"
    ./refresh_mirror.py -q || exit 1
    echo "Mirror refresh complete"
fi
git push --set-upstream origin master || exit 1
git checkout $branch || exit 1
