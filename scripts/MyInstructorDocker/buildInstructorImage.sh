#!/bin/bash
#
# Build an instructor container image for a given lab.
# First copies all required files to a staging directory in /tmp
#

lab=$1
if [ ! -d $lab ]; then
    echo "$lab not found as a lab directory"
    exit
fi
ORIG_PWD=`pwd`
echo $ORIG_PWD
LAB_DIR=${ORIG_PWD}/$lab/
LAB_TAR=${ORIG_PWD}/$lab.instructor.tar.gz
TMP_DIR=/tmp/$lab
rm -rf $TMP_DIR
mkdir $TMP_DIR
mkdir $TMP_DIR/.local
mkdir $TMP_DIR/.local/result
mkdir $TMP_DIR/.local/base

cp -r bin $TMP_DIR/.local/
cp -r $LAB_DIR/config $TMP_DIR/.local/ 2>>/dev/null
cd $TMP_DIR
tar --atime-preserve -zcvf $LAB_TAR .local *

cd $ORIG_PWD

docker build -f ${ORIG_PWD}/Dockerfile.$lab.instructor -t $lab:instructor .
