#!/bin/bash
#
# Build an instructor container image for a given lab.
# First copies all required files to a staging directory in /tmp
#

# Usage: buildInstructorImage.sh <labname> [<imagename>]
#        <imagename> is optional for lab that only has one image
lab=$1
if [ "$#" -eq 2 ]; then
    imagename=$2
    labimage=$lab.$imagename.instructor
else
    imagename=$lab
    labimage=$lab.$lab.instructor
fi

echo "Labname is $lab with image name $imagename"

LAB_TOP=`realpath ../../labs`
LAB_DIR=$LAB_TOP/$lab
if [ ! -d $LAB_DIR ]; then
    echo "$LAB_DIR not found as a lab directory"
    exit
fi
LABIMAGE_DIR=`realpath ../../labs/$lab/$imagename/`
if [ ! -d $LABIMAGE_DIR ]; then
    echo "$LABIMAGE_DIR not found"
    exit
fi
fixresolve='../../setup_scripts/fixresolv.sh'
if [ -f $fixresolve ]; then
    $fixresolve
fi
ORIG_PWD=`pwd`
echo $ORIG_PWD
LAB_TAR=$LAB_DIR/$labimage.tar.gz
TMP_DIR=/tmp/$labimage
rm -rf $TMP_DIR
mkdir $TMP_DIR
mkdir $TMP_DIR/.local
mkdir $TMP_DIR/.local/result
mkdir $TMP_DIR/.local/base
mkdir $TMP_DIR/.local/instr_config
mkdir $TMP_DIR/.local/config

cp -r bin $TMP_DIR/.local/
cp  $LAB_DIR/bin/* $TMP_DIR/.local/bin 2>>/dev/null
cp ../MyStudentDocker/bin/ParameterParser.py $TMP_DIR/.local/bin/
cp $LABIMAGE_DIR/* $TMP_DIR/
cp $LABIMAGE_DIR/.* $TMP_DIR/ 2>>/dev/null
cp $LAB_DIR/instr_config/* $TMP_DIR/.local/instr_config/ 2>>/dev/null
cp $LAB_DIR/config/* $TMP_DIR/.local/config/ 2>>/dev/null
cp config/* $TMP_DIR/.local/instr_config/ 2>>/dev/null
cd $TMP_DIR
pwd
#tar --atime-preserve -zcvf $LAB_TAR .local .
echo tar --atime-preserve -zcvf $LAB_TAR .
tar --atime-preserve -zcvf $LAB_TAR .

cd $LAB_TOP
dfile=Dockerfile.$labimage
docker build --build-arg lab=$labimage --build-arg labdir=$lab --build-arg imagedir=$imagename -f $LAB_DIR/dockerfiles/$dfile -t $labimage .
echo "removing temporary $dfile, reference original in $LAB_DIR/dockerfiles/$dfile"

cd $ORIG_PWD
