#!/bin/bash
lab=$1
LAB_DIR=`realpath ../../labs/$lab/`
if [ ! -d $LAB_DIR ]; then
    echo "$LAB_DIR not found as a lab directory"
    exit
fi
ORIG_PWD=`pwd`
echo $ORIG_PWD
#LAB_DIR=${ORIG_PWD}/$lab/
LAB_TAR=${ORIG_PWD}/$lab.student.tar.gz
TMP_DIR=/tmp/$lab
rm -rf $TMP_DIR
mkdir $TMP_DIR
mkdir $TMP_DIR/.local
cp $LAB_DIR/* $TMP_DIR 2>>/dev/null
cp -r $LAB_DIR/config $TMP_DIR/.local/ 2>>/dev/null
cp  -r bin/ $TMP_DIR/.local/  2>>/dev/null
cp  $LAB_DIR/bin/* $TMP_DIR/.local/bin 2>>/dev/null
mkdir $TMP_DIR/.local/result
cd $TMP_DIR
tar --atime-preserve -zcvf $LAB_TAR .local *
cd $ORIG_PWD
dfile=Dockerfile.$lab.student
cp $LAB_DIR/dockerfiles/$dfile .
docker build --build-arg lab=$lab -f ./$dfile -t $lab:student .
echo "removing temporary $dfile, reference original in $LAB_DIR/dockerfiles/$dfile"
rm ./$dfile
