#!/bin/bash

ORIG_PWD=`pwd`
echo $ORIG_PWD
PARAMLABS_DIR=${ORIG_PWD}/paramlabs/
PARAMLABS_TAR=${ORIG_PWD}/paramlabs.student.tar.gz
BUFOVERFLOW_DIR=${ORIG_PWD}/bufoverflow/
BUFOVERFLOW_TAR=${ORIG_PWD}/bufoverflow.student.tar.gz

cp -r bin $PARAMLABS_DIR/.local/
cp -r bin $BUFOVERFLOW_DIR/.local/
cd $PARAMLABS_DIR
tar -zcvf $PARAMLABS_TAR .local *
cd $BUFOVERFLOW_DIR
tar -zcvf $BUFOVERFLOW_TAR .local *

cd $ORIG_PWD

docker build -f ${ORIG_PWD}/Dockerfile.paramlabs.student -t paramlabs:student .
docker build -f ${ORIG_PWD}/Dockerfile.bufoverflow.student -t bufoverflow:student .
