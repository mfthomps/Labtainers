#!/bin/bash

PWD=`pwd`
echo $PWD
PARAMLABS_DIR=${PWD}/paramlabs/
PARAMLABS_TAR=${PWD}/paramlabs.instructor.tar.gz

cd $PARAMLABS_DIR
tar -zcvf $PARAMLABS_TAR .local *

cd $PWD

docker build -f ./Dockerfile.paramlabs.instructor -t paramlabs:instructor .
#docker build -f ./Dockerfile.bufoverflow.instructor -t bufoverflow:instructor .
