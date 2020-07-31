#!/bin/bash

echo Current Directory:
pwd
cd $1
echo Changed Directroy to:
pwd
echo Making lab: 
echo $2
mkdir $2
cd $2
new_lab_setup.py -b $3
echo Made new lab:
pwd

