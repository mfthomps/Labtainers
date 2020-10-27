#!/bin/bash
#
# Create a master Labtainer image for use in running Labtainers from a container
# on any system that has Docker installed, withou having to install Labtainers.
# Thanks for Olivier Berger for this contribution.
#
here=`pwd`
cd ../
mkdir -p workspace_master
rm -fr workspace_master/*
cp -a $LABTAINER_DIR/headless-lite/Dockerfile.labtainer.headless.tester workspace_master/Dockerfile.labtainer.headless.tester
cd workspace_master

CACHE="--no-cache"
LABTAINER_DEV="FALSE"
while [[ -n "$1" ]]; do
    if [[ "$1" == -h ]]; then
        echo "use -c to build with cache"
        echo "use -d to build developer version, otherwise pulls from distribution"
        exit 0
    fi
    if [[ "$1" == -c ]]; then
        CACHE=""
        shift
    fi
done
cp -a $LABTAINER_DIR/distrib/labtainer-tests.tar ./
docker build $CACHE --build-arg DOCKER_GROUP_ID="$(getent group docker | cut -d: -f3)" -f Dockerfile.labtainer.headless.tester -t labtainer.headless.tester:latest .
docker tag labtainer.headless.tester testregistry:5000/labtainer.headless.tester
echo "now push testregistry:5000/labtainer.headless.tester"
cd $here
