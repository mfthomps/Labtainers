#!/bin/bash
azdir=$HOME/labtainers_azure
mkdir -p $azdir
cd $azdir
wget --quiet https://github.com/mfthomps/Labtainers/releases/latest/download/azure.tar -O /tmp/azure.tar
tar -xf /tmp/azure.tar
echo "Labtainers for Azure scripts installed in $azdir"
echo "cd to that directory and run ./create_vm.sh, passsing in a user name"

