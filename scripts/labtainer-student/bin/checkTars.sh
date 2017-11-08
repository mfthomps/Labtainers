#!/bin/bash
#
# for each directory beneath the given one that ends in _tar
# tar up its content into a file based on the name of the
# subdirectory.  WILL remove existing tar file unless
# the directory only contains that tar file.
# The tarfile name is dirname[:-4]
#
LAB_DIR=$1
IMAGE_NAME=$2
echo "lab dir is $LAB_DIR"
here=`pwd`
tar_list=$(ls $LAB_DIR)
manifest_name="$IMAGE_NAME"-home_tar.list
#manifest=../../config/$manifest_name
manifest=$LAB_DIR/../config/$manifest_name
echo "manifest is $manifest"
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
                f_list=$(ls -a)
                if [[ -z $f_list ]];then
                     tar cvf $tar_name --files-from /dev/null
                else
                    if [[ $f == "home_tar" ]]; then
                        tar czf $tar_name . > $manifest
                    else
                        tar czf $tar_name .
                    fi
                fi
            else
                # has a tar file
                f_list=$(ls -at)
                f_array=($f_list)
                len=${#f_array[@]}
                if [[ $len -gt 1 ]] && [[ $tar_name != ${f_array[0]} ]] ; then
                    echo "replace tar"
                    rm $tar_name 2> /dev/null
                    if [[ $f == "home_tar" ]]; then
                        tar czf $tar_name . > $manifest
                    else
                        tar czf $tar_name .
                    fi
                elif [[ $len -eq 1 ]]; then
                    if [[ $f == "home_tar" ]]; then
                        echo "just one, update manifest"
                        tar tf $tar_name > $manifest
                    fi
                    if [[ -h $f_list ]]; then
                       # just this tar, and is a sym link, copy actual file
                       echo just this tar, and is a sym link, copy actual file
                       cp $f_list tmp.tar
                       mv tmp.tar $f_list
                    fi
                else
                    echo tar is newer
                fi
            fi
        fi
    fi
done
