#!/bin/bash

ORIG_PWD=`pwd`
echo $ORIG_PWD
PARAMLABS_DIR=${ORIG_PWD}/paramlabs/
PARAMLABS_TAR=${ORIG_PWD}/paramlabs.instructor.tar.gz
BUFOVERFLOW_DIR=${ORIG_PWD}/bufoverflow/
BUFOVERFLOW_TAR=${ORIG_PWD}/bufoverflow.instructor.tar.gz

cp -r bin $PARAMLABS_DIR/.local/
cd $PARAMLABS_DIR
tar -zcvf $PARAMLABS_TAR .local *
cp -r bin $BUFOVERFLOW_DIR/.local/
cd $BUFOVERFLOW_DIR
tar -zcvf $BUFOVERFLOW_TAR .local *

cd $ORIG_PWD

#docker build -f ${ORIG_PWD}/Dockerfile.paramlabs.instructor -t paramlabs:instructor .
docker build -f ${ORIG_PWD}/Dockerfile.bufoverflow.instructor -t bufoverflow:instructor .
