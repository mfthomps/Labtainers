#!/bin/bash
#
# for each directory beneath the given one that ends in _tar
# tar up its content into a file based on the name of the
# subdirectory.  WILL remove any existing tar files unless
# the directory only contains one tar file.
#
containsElement () {
   local e match="$1"
   shift
   for e; do [[ "$e" == "$match" ]] && return 0; done
   return 1
}
if [[ -z "$1" ]]; then
    echo need a path to top of tmp labs
fi
TOP_DIR=$1
SKIP_LIST=$2
while read skip; do
   MY_SKIP="$MY_SKIP $(basename $skip)"
done <$SKIP_LIST
echo "my skip is $MY_SKIP"
echo "lab dir is $LAB_DIR"
skip_array=($MY_SKIP)
here=`pwd`
cd $TOP_DIR
lab_list=$(ls)
for lab in $lab_list; do
    if [[ ! -d $lab ]]; then
        continue
    fi
    containsElement $lab "${skip_array[@]}"
    result=$?
    if [[ $result == "0" ]]; then
        continue
    fi
    LAB_DIR=$TOP_DIR/$lab
    cd $LAB_DIR
    CONTAINER_LIST=$(ls)
    for CONTAINER_DIR in $CONTAINER_LIST; do
        tar_list=$(ls $CONTAINER_DIR)
        #echo $tar_list
        for f in $tar_list; do
            #echo check $f
            full=$LAB_DIR/$f
            if [[ -d $full ]]; then
                if [[ $f == *_tar ]]; then
                   cd $full
                   echo "in $full"
                   tmp_name=${f::-4}
                   tar_name=$tmp_name.tar
                   echo "look for tar_name $tar_name"
                   if [[ ! -f $tar_name ]]; then
                       echo "no $tar_name, make one"
                       tar czf /tmp/$tar_name *
                       rm -fr *
                       mv /tmp/$tar_name .
                   else
                       # is a tar file
                       f_list=$(ls -lt)
                       f_array=($f_list)
                       len=${#f_array[@]}
                       if [[ $len -gt 1 ]] && [[ $tar_name -ot ${f_array[1]} ]] ; then
                           echo "replace tar"
                           rm $tar_name 2> /dev/null
                           tar czf /tmp/$tar_name *
                           rm -fr *
                           mv /tmp/$tar_name .
                       else
                           echo tar is newer, keep it
                           mv $tar_name /tmp/
                           rm -fr *
                           mv /tmp/$tar_name .
                       fi
                    fi
                fi
            fi
        done # each _tar directory
    done # each container
done  #each lab
cd $here
