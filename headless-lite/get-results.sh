#!/bin/bash
echo "Retrieving Labtainer results from $1"
mkdir -p ~/labtainer_xfer
scp -r labtainer@$1:~/headless-labtainers/labtainer_xfer/* ~/labtainer_xfer/
