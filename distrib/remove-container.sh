#!/bin/bash
cont_list=$(docker ps -a | grep $1 | awk '{ print $1" }')
if [ ! -z "$cont_list" ]; then
    docker rm $cont_list
fi
image_list=$(docker images | grep $1 | awk '{ print $1":"$2 }')
if [ ! -z "$image_list" ]; then
    docker rmi -f $image_list
fi

