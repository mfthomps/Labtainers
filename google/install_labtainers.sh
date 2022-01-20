#!/bin/bash
gdir=$HOME/labtainers_google
mkdir -p "$gdir"
cd "$gdir"
curl -L https://github.com/mfthomps/Labtainers/releases/latest/download/google.tar --output /tmp/google.tar
tar -xf /tmp/google.tar
echo ""
echo "Labtainers for Google Cloud scripts installed in $gdir"
echo "cd to that directory and run ./create_vm.sh, passsing in a user name, e.g., "
echo "  ./create_vm.sh myname"
echo ""

