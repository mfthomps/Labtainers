#!/bin/bash
azdir=$HOME/labtainers_azure
mkdir -p "$azdir"
cd "$azdir"
curl -L https://github.com/mfthomps/Labtainers/releases/latest/download/azure.tar --output /tmp/azure.tar
tar -xf /tmp/azure.tar
echo ""
echo "Labtainers for Azure scripts installed in $azdir"
echo "cd to that directory and run ./create_vm.sh, passsing in a user name, e.g., "
echo "  ./create_vm.sh myname"
echo ""

