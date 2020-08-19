#!/bin/bash

cd $1
cd $2
new_lab_setup.py -d $3
cd dockerfiles
#delete the dockerfile associated with this container
rm Dockerfile.$2.$3.student
