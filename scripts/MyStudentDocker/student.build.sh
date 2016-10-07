#!/bin/bash

PWD=`pwd`
echo $PWD
PARAMLABS_DIR=${PWD}/paramlabs/
PARAMLABS_TAR=${PWD}/paramlabs.student.tar.gz
BUFOVERFLOW_DIR=${PWD}/bufoverflow/
BUFOVERFLOW_TAR=${PWD}/bufoverflow.student.tar.gz

cd $PARAMLABS_DIR
tar -zcvf $PARAMLABS_TAR .local *
cd $BUFOVERFLOW_DIR
tar -zcvf $BUFOVERFLOW_TAR .local *

cd $PWD

docker build -f ./Dockerfile.paramlabs.student -t paramlabs:student .
#docker build -f ./Dockerfile.bufoverflow.student -t bufoverflow:student .
