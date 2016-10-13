#!/bin/bash

ORIG_PWD=`pwd`
echo $ORIG_PWD
PARAMLABS_DIR=${ORIG_PWD}/paramlabs/
PARAMLABS_TAR=${ORIG_PWD}/paramlabs.instructor.tar.gz

cd $PARAMLABS_DIR
tar -zcvf $PARAMLABS_TAR .local *

cd $ORIG_PWD

docker build -f ${ORIG_PWD}/Dockerfile.paramlabs.instructor -t paramlabs:instructor .
#docker build -f ${ORIG_PWD}/Dockerfile.bufoverflow.instructor -t bufoverflow:instructor .
