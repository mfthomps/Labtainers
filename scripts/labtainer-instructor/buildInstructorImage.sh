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
# Usage: buildImage.sh <labname> <imagename> <user_name> <force_build>
#        <force_build> is either true or false

lab=$1
imagename=$2
labimage=$lab.$imagename.instructor
user_name=$3
force_build=$4 
LAB_TOP=$5 
APT_SOURCE=$6 

if [ "$#" -eq 7 ]; then
    registry=$7 
elif [ "$#" -eq 6 ]; then
    registry=mfthomps
else
    echo "Usage: buildImage.sh <labname> <imagename> <user_name> <force_build> <LAB_TOP> [registry]"
    echo "   <force_build> is either true or false"
    echo "   <LAB_TOP> is a path to the trunk/labs directory"
    echo "   <apt_source> is the host to use in apt/sources.list"
    echo "   registry is an optional name of an alternate docker hub registry"
    exit
fi

echo "LAB_TOP is $LAB_TOP"
echo "Labname is $lab with image name $imagename"

LAB_DIR=$LAB_TOP/$lab
if [ ! -d $LAB_DIR ]; then
    echo "$LAB_DIR not found as a lab directory"
    exit
fi
LABIMAGE_DIR=$LAB_TOP/$lab/$imagename/
if [ ! -d $LABIMAGE_DIR ]; then
    echo "$LABIMAGE_DIR not found"
    exit
fi

#-----------------------------------V
echo docker pull $registry/$labimage
docker pull $registry/$labimage
result=$?
if [ "$result" == "0" ] && [ $force_build = "False" ]; then
    imagecheck="YES"
    #create tmp folder
    if [ ! -d "$LAB_DIR/dockerfiles/tmp" ]; then
    	mkdir $LAB_DIR/dockerfiles/tmp
    fi
    #create tmp file
    echo "FROM $registry/$labimage" > $LAB_DIR/dockerfiles/tmp/Dockerfile.$labimage.tmp
else
    ORIG_PWD=`pwd`
    echo $ORIG_PWD
    ../labtainer-student/checkTars.sh $LAB_DIR
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
    cp  $LABIMAGE_DIR/_bin/* $TMP_DIR/.local/bin 2>>/dev/null
    chmod a+x $TMP_DIR/.local/bin/*
    cp -r $LABIMAGE_DIR/. $TMP_DIR 2>>/dev/null
    # ugly!
    rm -fr $TMP_DIR/_bin
    rm -fr $TMP_DIR/_system
    rm -fr $TMP_DIR/home_tar
    rm -fr $TMP_DIR/sys_tar
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
fi
#-------------------------------------------------------------------^
cd $LAB_TOP
dfile=Dockerfile.$labimage
full_dfile=$LAB_DIR/dockerfiles/$dfile
echo "full_file is $full_dfile"
if [ ! -f $full_dfile ]; then
   full_dfile=${full_dfile/instructor/student}
   echo "full_file now is $full_dfile"
fi

#--------------------------------V
if [ ! -z "$imagecheck" ] && [ $force_build = "False" ]; then 
    docker build --pull -f $LAB_DIR/dockerfiles/tmp/$dfile.tmp \
                 --build-arg https_proxy=$HTTP_PROXY --build-arg http_proxy=$HTTP_PROXY \
                 --build-arg HTTP_PROXY=$HTTP_PROXY --build-arg HTTPS_PROXY=$HTTP_PROXY \
                 --build-arg NO_PROXY=$NO_PROXY  --build-arg no_proxy=$NO_PROXY \
                 -t $labimage .
else
    docker build --build-arg lab=$labimage --build-arg labdir=$lab --build-arg imagedir=$imagename \
                 --build-arg user_name=$user_name --build-arg apt_source=$APT_SOURCE \
                 --build-arg https_proxy=$HTTP_PROXY --build-arg http_proxy=$HTTP_PROXY \
                 --build-arg HTTP_PROXY=$HTTP_PROXY --build-arg HTTPS_PROXY=$HTTP_PROXY \
                 --build-arg NO_PROXY=$NO_PROXY  --build-arg no_proxy=$NO_PROXY \
                 --pull -f $full_dfile -t $labimage .
fi
#--------------------------------^
echo "removing temporary $dfile, reference original in $LAB_DIR/dockerfiles/$dfile"

cd $ORIG_PWD
