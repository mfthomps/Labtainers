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

# Usage: buildImage.sh <labname> <imagename> <user_name> <user_password> <force_build> <lab_top>
#        <force_build> is either true or false

lab=$1
imagename=$2
labimage=$lab.$imagename.student
user_name=$3
user_password=$4
force_build=$5 
LAB_TOP=$6 
APT_SOURCE=$7 
REGISTRY=$8 
#------------------------------------V
if [ "$#" -ne 8 ]; then
    echo "Usage: buildImage.sh <labname> <imagename> <user_name> <user_password> <force_build> <LAB_TOP> <apt_source> <registry>"
    echo "   <force_build> is either true or false"
    echo "   <LAB_TOP> is a path to the trunk/labs directory"
    echo "   <apt_source> is the host to use in apt/sources.list"
    echo "   <registry> is a docker registry"
    exit
fi

#------------------------------------^

echo "Labname is $lab with image name $imagename"

LAB_DIR=$LAB_TOP/$lab
if [ ! -d $LAB_DIR ]; then
    echo "$LAB_DIR not found as a lab directory"
    exit
fi
#------------------------------------V
echo docker pull $REGISTRY/$labimage
docker pull $REGISTRY/$labimage
result=$?
if [ "$result" == "0" ] && [ $force_build = "False" ]; then
    imagecheck="YES"
else
    echo "Please wait while the lab is built"
    sleep 3
    LABIMAGE_DIR=$LAB_TOP/$lab/$imagename/
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
    cp -pr $LAB_DIR/config $TMP_DIR/.local/ 2>>/dev/null
    cp -pr lab_bin/ $TMP_DIR/.local/bin  2>>/dev/null
    cp -p $LAB_DIR/bin/* $TMP_DIR/.local/bin 2>>/dev/null
    chmod a+x $TMP_DIR/.local/bin/* 2>>/dev/null
    cp -p $LABIMAGE_DIR/_bin/* $TMP_DIR/.local/bin 2>>/dev/null
    chmod a+x $TMP_DIR/.local/bin/*
    cp -pr $LABIMAGE_DIR/. $TMP_DIR 2>>/dev/null
    # ugly!
    rm -fr $TMP_DIR/_bin
    rm -fr $TMP_DIR/_system
    rm -fr $TMP_DIR/home_tar
    rm -fr $TMP_DIR/sys_tar
    mkdir $TMP_DIR/.local/result
    if [ -d $LABIMAGE_DIR/_system ]; then
        cd $LABIMAGE_DIR/_system
        tar --atime-preserve -zcvf $SYS_TAR . > $TMP_DIR/.local/sys_manifest.list
    else
        echo nothing at $LABIMAGE_DIR/_system
        # make empty tar
        mkdir $LABIMAGE_DIR/_system
        cd -p $LABIMAGE_DIR/_system
        tar --atime-preserve -zcvf $SYS_TAR .
    fi
    # do after sys so we get manifest
    cd $TMP_DIR
    tar --atime-preserve -zcvf $LAB_TAR .
fi
#---------------------------------------------------------------^
cd $LAB_TOP
dfile=Dockerfile.$labimage
#---------------------------------V
result=0
if [ ! -z "$imagecheck" ] && [ $force_build = "False" ]; then 
#    docker build --pull -f $LAB_DIR/dockerfiles/tmp/$dfile.tmp \
#                 --build-arg https_proxy=$HTTP_PROXY --build-arg http_proxy=$HTTP_PROXY \
#                 --build-arg HTTP_PROXY=$HTTP_PROXY --build-arg HTTPS_PROXY=$HTTP_PROXY \
#                 --build-arg NO_PROXY=$NO_PROXY  --build-arg no_proxy=$NO_PROXY \
#              -t $labimage .
    echo "use exising image"
else
    echo docker build --build-arg lab=$labimage --build-arg labdir=$lab --build-arg imagedir=$imagename \
                 --build-arg user_name=$user_name --build-arg password=$user_password --build-arg apt_source=$APT_SOURCE \
                 --build-arg https_proxy=$HTTP_PROXY --build-arg http_proxy=$HTTP_PROXY \
                 --build-arg HTTP_PROXY=$HTTP_PROXY --build-arg HTTPS_PROXY=$HTTP_PROXY \
                 --build-arg NO_PROXY=$NO_PROXY  --build-arg no_proxy=$NO_PROXY \
                 --build-arg registry=$REGISTRY \
               --pull -f $LAB_DIR/dockerfiles/$dfile -t $labimage .
    docker build --build-arg lab=$labimage --build-arg labdir=$lab --build-arg imagedir=$imagename \
                 --build-arg user_name=$user_name --build-arg password=$user_password --build-arg apt_source=$APT_SOURCE \
                 --build-arg https_proxy=$HTTP_PROXY --build-arg http_proxy=$HTTP_PROXY \
                 --build-arg HTTP_PROXY=$HTTP_PROXY --build-arg HTTPS_PROXY=$HTTP_PROXY \
                 --build-arg NO_PROXY=$NO_PROXY  --build-arg no_proxy=$NO_PROXY \
                 --build-arg registry=$REGISTRY \
               --pull -f $LAB_DIR/dockerfiles/$dfile -t $labimage .
    result=$?
fi
#---------------------------------^
echo "removing temporary $dfile, reference original in $LAB_DIR/dockerfiles/$dfile"
#rm $LABIMAGE_DIR
cd $ORIG_PWD
if [ $result != 0 ]; then
    echo "Error in docker build result $result"
    exit 1
fi
