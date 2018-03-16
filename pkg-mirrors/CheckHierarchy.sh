#!/usr/bin/env bash
#
# Filename: CheckHierarchy.sh
#
# Assumptions:
# 1. /var/www/html/ubuntumirror.uc.nps.edu/ubuntu has been created


if [[ $EUID -ne 0 ]]
then
    echo "This script must be run as root"
    exit 1
fi

UBUNTUBASE="/var/www/html/ubuntumirror.uc.nps.edu/ubuntu"
TMPDIR="/tmp/.checkhierarchy"
CURRENTDIR=`pwd`

/usr/bin/rm -rf $TMPDIR
/usr/bin/mkdir -p $TMPDIR

if [ ! -d "$UBUNTUBASE" ]
then
    echo "$UBUNTUBASE DOES NOT exist"
    exit 1
fi

PATH=""
RESULTSTATUS="OK"
TOP=("xenial" "xenial-updates")
VARIANT=("main" "restricted" "universe" "multiverse")
ARCHDEP=("binary-amd64" "i18n" "dep11")
for i in "${TOP[@]}";
do
    for j in "${VARIANT[@]}";
    do
        for k in "${ARCHDEP[@]}";
        do
            DIRNAME="$UBUNTUBASE/dists/$i/$j/$k"
            /usr/bin/rm -rf $DIRNAME
        done
    done
done
for i in "${TOP[@]}";
do
    for j in "${VARIANT[@]}";
    do
        for k in "${ARCHDEP[@]}";
        do
            DIRNAME="$UBUNTUBASE/dists/$i/$j/$k"
            PARENTPATH="$UBUNTUBASE/dists/$i/$j"
            TMPDIRPATH="$TMPDIR/us.archive.ubuntu.com/ubuntu/dists/$i/$j/$k"
            PATH="http://us.archive.ubuntu.com/ubuntu/dists/$i/$j/$k"
            if [ ! -d "$DIRNAME" ]
            then
                echo "DIRNAME ($DIRNAME) DOES NOT exist"
                cd $TMPDIR
                /usr/bin/mkdir -p $PARENTPATH
                /usr/bin/wget -r -l 1 $PATH
                /usr/bin/mv $TMPDIRPATH $PARENTPATH
                cd $CURRENTDIR
                /usr/bin/rm -rf $TMPDIR
                /usr/bin/mkdir -p $TMPDIR
            fi
        done
    done
done
for i in "${TOP[@]}";
do
    for j in "${VARIANT[@]}";
    do
        PACKAGENAME="$UBUNTUBASE/dists/$i/$j/binary-amd64/Packages"
        PACKAGENAMEGZ="$UBUNTUBASE/dists/$i/$j/binary-amd64/Packages.gz"
        PACKAGENAMEXZ="$UBUNTUBASE/dists/$i/$j/binary-amd64/Packages.xz"
        PATH="http://us.archive.ubuntu.com/ubuntu/dists/$i/$j/binary-amd64"
        if [ ! -f "$PACKAGENAME" ]
        then
            echo "PACKAGENAME ($PACKAGENAME) DOES NOT exist"
            if [ -f "$PACKAGENAMEGZ" ]
            then
                cd $TMPDIR
                /usr/bin/cp $PACKAGENAMEGZ $TMPDIR/Packages.gz
                /usr/bin/gzip -d $TMPDIR/Packages.gz
                /usr/bin/mv $TMPDIR/Packages $PACKAGENAME
                cd $CURRENTDIR
                /usr/bin/rm -rf $TMPDIR
                /usr/bin/mkdir -p $TMPDIR
            else
                if [ -f "$PACKAGENAMEXZ" ]
                then
                    cd $TMPDIR
                    /usr/bin/cp $PACKAGENAMEGZ $TMPDIR/Packages.xz
                    /usr/bin/unxz $TMPDIR/Packages.xz
                    /usr/bin/mv $TMPDIR/Packages $PACKAGENAME
                    cd $CURRENTDIR
                    /usr/bin/rm -rf $TMPDIR
                    /usr/bin/mkdir -p $TMPDIR
                else
                    RESULTSTATUS="NOTOK"
                    break
                fi
            fi
        fi
    done
    if [ "$RESULTSTATUS" == "NOTOK" ]
    then
        break
    fi
done
if [ "$RESULTSTATUS" == "OK" ]
then
    for j in "${VARIANT[@]}";
    do
        DIRNAME="$UBUNTUBASE/pool/$j"
        PATH="$UBUNTUBASE/pool/$j"
        if [ ! -d "$DIRNAME" ]
        then
            echo "DIRNAME ($DIRNAME) DOES NOT exist"
            RESULTSTATUS="NOTOK"
            /usr/bin/mkdir -p $PATH
        fi
    done
fi

/usr/bin/chown -R apache:apache $UBUNTUBASE/dists $UBUNTUBASE/pool
echo "RESULTSTATUS is ($RESULTSTATUS)"
