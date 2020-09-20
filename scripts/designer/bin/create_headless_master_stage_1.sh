#!/bin/bash
#
# Create a master Labtainer image for use in running Labtainers from a container
# on any system that has Docker installed, withou having to install Labtainers.
# Thanks for Olivier Berger for this contribution.
#
source ./set_reg.sh
if [[ "$1" != -f ]]; then
   echo "This will build the labtainer master controller image.  "
   echo "registry is $LABTAINER_REGISTRY"
   read -p "Continue? (y/n)"
   if [[ ! $REPLY =~ ^[Yy]$ ]]
   then
       echo exiting
       exit
   fi
else
   echo "registry is $LABTAINER_REGISTRY"
fi
here=`pwd`
cd ../
mkdir -p workspace_master
cp -a $LABTAINER_DIR/headless-lite/Dockerfile.labtainer.master workspace_master/Dockerfile.labtainer.headless
cp -aR workspace/system workspace_master/
cp -a $LABTAINER_DIR/headless-lite/motd workspace_master
cp -a $LABTAINER_DIR/headless-lite/docker-entrypoint workspace_master
cp -a  $LABTAINER_DIR/headless-lite/wait-for-it.sh workspace_master
cp -a  $LABTAINER_DIR/headless-lite/doterm.sh workspace_master
cd workspace_master
cp -a $LABTAINER_DIR/distrib/labtainer.tar ./

cat <<EOT >bashrc.labtainer.master
   if [[ ":\$PATH:" != *":./bin:"* ]]; then 
       export PATH="\${PATH}:./bin:/home/labtainer/labtainer/trunk/scripts/designer/bin"
       export LABTAINER_DIR=/home/labtainer/labtainer/trunk
   fi
EOT

cp $LABTAINER_DIR/scripts/labtainer-student/bin/labutils.py ./
#docker build --no-cache --build-arg DOCKER_GROUP_ID="$(getent group docker | cut -d: -f3)" -f Dockerfile.labtainer.headless -t labtainer.master:latest .
CACHE="--no-cache"
if [[ "$1" == -c ]]; then
    CACHE=""
fi
docker build $CACHE --build-arg DOCKER_GROUP_ID="$(getent group docker | cut -d: -f3)" -f Dockerfile.labtainer.headless -t labtainer.master:stage.1 .
cd $here
