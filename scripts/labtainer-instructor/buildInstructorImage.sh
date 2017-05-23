#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
END
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
SYS_TAR=$LAB_DIR/sys_$labimage.tar.gz
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
cp ../labtainer-student/bin/ParameterParser.py $TMP_DIR/.local/bin/
cp -r $LABIMAGE_DIR/. $TMP_DIR 2>>/dev/null
# ugly!
rm -fr $TMP_DIR/_bin
rm -fr $TMP_DIR/_system
cp $LAB_DIR/instr_config/* $TMP_DIR/.local/instr_config/ 2>>/dev/null
cp $LAB_DIR/config/* $TMP_DIR/.local/config/ 2>>/dev/null
cp config/* $TMP_DIR/.local/instr_config/ 2>>/dev/null
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
full_dfile=$LAB_DIR/dockerfiles/$dfile
echo "full_file is $full_dfile"
if [ ! -f $full_dfile ]; then
   full_dfile=${full_dfile/instructor/student}
   echo "full_file now is $full_dfile"
fi
docker build --build-arg lab=$labimage --build-arg labdir=$lab --build-arg imagedir=$imagename --pull -f $full_dfile -t $labimage .
echo "removing temporary $dfile, reference original in $LAB_DIR/dockerfiles/$dfile"

cd $ORIG_PWD
