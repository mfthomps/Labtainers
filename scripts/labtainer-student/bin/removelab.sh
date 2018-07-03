#!/bin/bash
cont_list=$(docker ps -a | grep " $1\." | awk '{print $1}')
if [[ ! -z "$cont_list" ]]; then
    #echo docker rm $cont_list
    docker rm $cont_list
fi
image_list=$(docker images | grep "/$1\." | awk '{ print $1":"$2 }')
if [[ ! -z "$image_list" ]] && [[ "$image_list" != *\<none\>* ]]; then
    #echo docker rmi -f $image_list
    docker rmi -f $image_list
else
    echo "No images for $1"
fi
image_list=$(docker images | grep "^$1\." | awk '{ print $1":"$2 }')
if [[ ! -z "$image_list" ]] && [[ "$image_list" != *\<none\>* ]]; then
    #echo docker rmi -f $image_list
    docker rmi -f $image_list
else
    echo "No images for $1"
fi
