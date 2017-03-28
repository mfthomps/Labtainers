#!/bin/bash

# Usage: buildImage.sh <labname> [<imagename>]
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
LAB_TAR=${ORIG_PWD}/$labimage.student.tar.gz
TMP_DIR=/tmp/$labimage
rm -rf $TMP_DIR
mkdir $TMP_DIR
mkdir $TMP_DIR/.local
cp $LABIMAGE_DIR/* $TMP_DIR 2>>/dev/null
cp -r $LAB_DIR/config $TMP_DIR/.local/ 2>>/dev/null
cp  -r bin/ $TMP_DIR/.local/  2>>/dev/null
cp  $LAB_DIR/bin/* $TMP_DIR/.local/bin 2>>/dev/null
cp  $LABIMAGE_DIR/bin/* $TMP_DIR/.local/bin 2>>/dev/null
mkdir $TMP_DIR/.local/result
cd $TMP_DIR
tar --atime-preserve -zcvf $LAB_TAR .local *
cd $ORIG_PWD
dfile=Dockerfile.$labimage.student
cp $LAB_DIR/dockerfiles/$dfile .

docker build --build-arg lab=$labimage -f ./$dfile -t $labimage:student .
echo "removing temporary $dfile, reference original in $LAB_DIR/dockerfiles/$dfile"
rm ./$dfile
