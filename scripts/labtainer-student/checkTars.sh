#!/bin/bash
#
# for each directory beneath the given one that ends in _tar
# tar up its content into a file based on the name of the
# subdirectory.  WILL remove existing tar file unless
# the directory only contains that tar file.
# The tarfile name is dirname[:-4]
#
LAB_DIR=$1
echo "lab dir is $LAB_DIR"
here=`pwd`
tar_list=$(ls $LAB_DIR)
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
                f_list=$(ls)
                if [[ -z $f_list ]];then
                    touch $tar_name
                else
                    if [[ $f == "home_tar" ]]; then
                        tar czvf $tar_name * > ../../config/home_tar.list
                    else
                        tar czf $tar_name *
                    fi
                fi
            else
                # has a tar file
                f_list=$(ls -lt)
                f_array=($f_list)
                len=${#f_array[@]}
                if [[ $len -gt 1 ]] && [[ $tar_name -ot ${f_array[1]} ]] ; then
                    echo "replace tar"
                    rm $tar_name 2> /dev/null
                    if [[ $f == "home_tar" ]]; then
                        tar czvf $tar_name * >> ../../config/home_tar.list
                    else
                        tar czf $tar_name *
                    fi
                else
                    echo tar is newer
                fi
            fi
        fi
    fi
done
