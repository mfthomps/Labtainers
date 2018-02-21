#!/bin/bash
#
# pull the baseline labtainer images from the appropriate registry
# NOTE use of environment variable TEST_REGISTRY
# Script assumes the pwd is the parent of the labtainer directory
# Intended to be called from update-labtainer.sh
#
if [ "$TEST_REGISTRY" == TRUE ] || [ "$1" == -t ]; then
    registry=$(grep TEST_REGISTRY ../config/labtainer.config | tr -s ' ' | cut -d ' ' -f 3)
else
    registry=$(grep DEFAULT_REGISTRY ../config/labtainer.config | tr -s ' ' | cut -d ' ' -f 3)
fi
echo "pull from $registry"
docker pull $registry/labtainer.base
docker pull $registry/labtainer.network
docker pull $registry/labtainer.firefox
docker pull $registry/labtainer.wireshark
docker pull $registry/labtainer.java
docker pull $registry/labtainer.centos
docker pull $registry/labtainer.lamp
