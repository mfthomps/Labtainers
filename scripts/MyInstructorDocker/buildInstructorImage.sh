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
    labimage=$lab.$imagename
else
    imagename=$lab
    labimage=$lab.$lab
fi

echo "Labname is $lab with image name $imagename"

LAB_DIR=`realpath ../../labs/$lab/`
if [ ! -d $LAB_DIR ]; then
    echo "$LAB_DIR not found as a lab directory"
    exit
fi
LABIMAGE_DIR=`realpath ../../labs/$lab/$imagename/`
if [ ! -d $LABIMAGE_DIR ]; then
    echo "$LABIMAGE_DIR not found"
    exit
fi
ORIG_PWD=`pwd`
echo $ORIG_PWD
LAB_TAR=${ORIG_PWD}/$labimage.instructor.tar.gz
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
cp $LAB_DIR/instr_config/* $TMP_DIR/.local/instr_config/ 2>>/dev/null
cp $LAB_DIR/config/* $TMP_DIR/.local/config/ 2>>/dev/null
cp config/* $TMP_DIR/.local/instr_config/ 2>>/dev/null
cd $TMP_DIR
pwd
echo tar --atime-preserve -zcvf $LAB_TAR .local *
tar --atime-preserve -zcvf $LAB_TAR .local *

cd $ORIG_PWD
dfile=Dockerfile.$labimage.instructor
cp $LAB_DIR/dockerfiles/$dfile .
fixresolve='../../setup_scripts/fixresolv.sh'
if [ -f $fixresolve ]; then
    $fixresolve
fi
docker build --build-arg lab=$labimage --build-arg labdir=$LABIMAGE_DIR -f ./$dfile -t $labimage:instructor .
echo "removing temporary $dfile, reference original in $LAB_DIR/dockerfiles/$dfile"
rm ./$dfile

