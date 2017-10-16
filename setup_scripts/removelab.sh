#!/bin/bash
cont_list=$(docker ps -a | grep $1 | awk '{print $1}')
echo $cont_list
docker rm $cont_list
image_list=$(docker images | grep $1 | awk '{print $1}')
docker rmi -f $image_list
