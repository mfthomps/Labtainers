#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

END


lab=$1
imagename=$2
labimage=$lab.$imagename.student
user_name=$3
user_password=$4
force_build=$5 
LAB_TOP=$6 
APT_SOURCE=$7 
REGISTRY=$8 
VERSION=$9 
shift 1
NO_PULL=$9
shift 1
USE_CACHE=$9
if [ "$#" -ne 9 ]; then
    echo "Usage: buildImage.sh <labname> <imagename> <user_name> <user_password> <force_build> <LAB_TOP> <apt_source> <registry>"
    echo "   <force_build> is either true or false"
    echo "   <LAB_TOP> is a path to the trunk/labs directory"
    echo "   <apt_source> is the host to use in apt/sources.list"
    echo "   <registry> is a docker registry"
    echo "   <version> is the framework version needed to run this lab"
    echo "   <no_pull> is 'True' to avoid pulling images, e.g., no internet acess"
    exit
fi
mkdir -p $LABTAINER_DIR/logs
exec &> >(tee -a "$LABTAINER_DIR/logs/docker_build.log")
echo "Labname is $lab with image name $imagename"

LAB_DIR=$LAB_TOP/$lab
if [ ! -d $LAB_DIR ]; then
    echo "$LAB_DIR not found as a lab directory"
    exit
fi
#echo "force_build is $force_build"
if [ $force_build == "False" ]; then
    echo docker pull $REGISTRY/$labimage
    docker pull $REGISTRY/$labimage
    result=$?
fi
if [ "$result" == "0" ] && [ $force_build = "False" ]; then
    imagecheck="YES"
else
    echo "Please wait while the lab is built"
    #sleep 3
    LABIMAGE_DIR=$LAB_TOP/$lab/$imagename/
    if [ ! -d $LABIMAGE_DIR ]; then
        echo "$LABIMAGE_DIR not found"
        exit
    fi
    ORIG_PWD=`pwd`
    echo "ORIG_PWD is:" $ORIG_PWD
    LAB_TAR=$LABIMAGE_DIR/$labimage.tar.gz
    SYS_TAR=$LABIMAGE_DIR/sys_$labimage.tar.gz
    rm -f $LAB_TAR
    rm -f $SYS_TAR
    TMP_DIR=$(mktemp /tmp/$labimage.XXXXXX)
    rm -rf $TMP_DIR
    mkdir $TMP_DIR
    mkdir $TMP_DIR/.local
    mkdir $TMP_DIR/.local/bin
    cp -pr $LAB_DIR/config $TMP_DIR/.local/ 2>>/dev/null
    #cp -pr lab_bin/ $TMP_DIR/.local/bin  2>>/dev/null
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
        tar --atime-preserve -czvf $SYS_TAR . > $TMP_DIR/.local/sys_manifest.list
    else
        echo nothing at $LABIMAGE_DIR/_system
        # make empty tar
        mkdir $LABIMAGE_DIR/_system
        cd -p $LABIMAGE_DIR/_system
        tar --atime-preserve -czvf $SYS_TAR .
    fi
    #cd $ORIG_PWD/lab_sys
    #tar --append --file=$SYS_TAR * 
    #gzip -f $SYS_TAR
    # do after sys so we get manifest
    cd $TMP_DIR
    tar --atime-preserve -zcvf $LAB_TAR .
fi
#cd $LAB_TOP
cd $LABIMAGE_DIR
dfile=Dockerfile.$labimage
result=0
pull="--pull"
if [ "$NO_PULL" == "True" ]; then
    pull=''
fi
cache=""
if [ "$USE_CACHE" == "False" ]; then
    cache="--no-cache"
fi
if [ ! -z "$imagecheck" ] && [ $force_build = "False" ]; then 
    echo "use exising image"
else
    cp ../dockerfiles/$dfile .
    if [[ $REGISTRY == "LOCAL" ]]; then
        echo "using local registry"
        sed -i 's/$registry\///' Docker*
    fi
    echo docker build $cache --build-arg lab=$labimage --build-arg labdir="." --build-arg imagedir="." \
                 --build-arg user_name=$user_name --build-arg password=$user_password --build-arg apt_source=$APT_SOURCE \
                 --build-arg https_proxy=$HTTP_PROXY --build-arg http_proxy=$HTTP_PROXY \
                 --build-arg HTTP_PROXY=$HTTP_PROXY --build-arg HTTPS_PROXY=$HTTP_PROXY \
                 --build-arg NO_PROXY=$NO_PROXY  --build-arg no_proxy=$NO_PROXY \
                 --build-arg registry=$REGISTRY --build-arg version=$VERSION \
               $pull -f $dfile -t $labimage .
    date
    docker build $cache --build-arg lab=$labimage --build-arg labdir="." --build-arg imagedir="." \
                 --build-arg user_name=$user_name --build-arg password=$user_password --build-arg apt_source=$APT_SOURCE \
                 --build-arg https_proxy=$HTTP_PROXY --build-arg http_proxy=$HTTP_PROXY \
                 --build-arg HTTP_PROXY=$HTTP_PROXY --build-arg HTTPS_PROXY=$HTTP_PROXY \
                 --build-arg NO_PROXY=$NO_PROXY  --build-arg no_proxy=$NO_PROXY \
                 --build-arg registry=$REGISTRY --build-arg version=$VERSION \
               $pull -f $dfile -t $labimage .
    result=$?
fi

rm $dfile
echo "removing temporary $dfile, reference original in $LAB_DIR/dockerfiles/$dfile"
#rm $LABIMAGE_DIR
cd $ORIG_PWD
if [ $result != 0 ]; then
    date
    echo "Error in docker build result $result"
    exit 1
fi
