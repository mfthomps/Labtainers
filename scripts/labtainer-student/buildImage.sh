#!/bin/bash

# Usage: buildImage.sh <labname> [<imagename>]
#        <imagename> is optional for lab that only has one image
lab=$1
if [ "$#" -eq 2 ]; then
    imagename=$2
    labimage=$lab.$imagename.student
else
    imagename=$lab
    labimage=$lab.$lab.student
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

ORIG_PWD=`pwd`
echo $ORIG_PWD
LAB_TAR=$LAB_DIR/$labimage.tar.gz
SYS_TAR=$LAB_DIR/sys_$labimage.tar.gz
TMP_DIR=/tmp/$labimage
rm -rf $TMP_DIR
mkdir $TMP_DIR
mkdir $TMP_DIR/.local
cp -r $LABIMAGE_DIR/. $TMP_DIR 2>>/dev/null
# ugly!
rm -fr $TMP_DIR/_bin
rm -fr $TMP_DIR/_system
cp -r $LAB_DIR/config $TMP_DIR/.local/ 2>>/dev/null
cp  -r bin/ $TMP_DIR/.local/  2>>/dev/null
cp  $LAB_DIR/bin/* $TMP_DIR/.local/bin 2>>/dev/null
chmod a+x $TMP_DIR/.local/bin/* 2>>/dev/null
cp  $LABIMAGE_DIR/_bin/* $TMP_DIR/.local/bin 2>>/dev/null
mkdir $TMP_DIR/.local/result
cd $TMP_DIR
tar --atime-preserve -zcvf $LAB_TAR .
if [ -d $LABIMAGE_DIR/_system ]; then
    cd $LABIMAGE_DIR/_system
    tar --atime-preserve -zcvf $SYS_TAR .
else
    echo nothing at $LABIMAGE_DIR/_system
    mkdir $LABIMAGE_DIR/_system
    cd $LABIMAGE_DIR/_system
    tar --atime-preserve -zcvf $SYS_TAR .
fi
cd $LAB_TOP
dfile=Dockerfile.$labimage
docker build --build-arg lab=$labimage --build-arg labdir=$lab --build-arg imagedir=$imagename -f $LAB_DIR/dockerfiles/$dfile -t $labimage .
result=$?
echo "removing temporary $dfile, reference original in $LAB_DIR/dockerfiles/$dfile"
#rm $LABIMAGE_DIR
cd $ORIG_PWD
if [ $result != 0 ]; then
    echo "Error in docker build result $result"
    exit 1
fi
