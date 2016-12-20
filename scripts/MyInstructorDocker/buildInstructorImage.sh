#!/bin/bash
#
# Build an instructor container image for a given lab.
# First copies all required files to a staging directory in /tmp
#
lab=$1
lab=$1
LAB_DIR=`realpath ../../labs/$lab/`
if [ ! -d $LAB_DIR ]; then
    echo "$LAB_DIR not found as a lab directory"
    exit
fi
ORIG_PWD=`pwd`
echo $ORIG_PWD
#LAB_DIR=${ORIG_PWD}/$lab/
LAB_TAR=${ORIG_PWD}/$lab.instructor.tar.gz
TMP_DIR=/tmp/$lab
rm -rf $TMP_DIR
mkdir $TMP_DIR
mkdir $TMP_DIR/.local
mkdir $TMP_DIR/.local/result
mkdir $TMP_DIR/.local/base
mkdir $TMP_DIR/.local/instr_config

cp -r bin $TMP_DIR/.local/
cp $LAB_DIR/* $TMP_DIR/
cp $LAB_DIR/instr_config/* $TMP_DIR/.local/instr_config/ 2>>/dev/null
cp config/* $TMP_DIR/.local/instr_config/ 2>>/dev/null
cd $TMP_DIR
pwd
echo tar --atime-preserve -zcvf $LAB_TAR .local *
tar --atime-preserve -zcvf $LAB_TAR .local *

cd $ORIG_PWD
dfile=Dockerfile.$lab.instructor
cp $LAB_DIR/dockerfiles/$dfile .
docker build -f ./$dfile -t $lab:instructor .
echo "removing temporary $dfile, reference original in $LAB_DIR/dockerfiles/$dfile"
rm ./$dfile

