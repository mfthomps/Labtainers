#!/bin/bash
# Assume running from setup_scripts/
#Clear out docker.
now=`date +"%s"`
exec > /media/sf_SEED/smokelogs/log-$now.log
exec 2>&1
./destroy-docker.sh -f

# Update baseline and framework
./update-labtainer.sh -t

# Update test sets
./update-testsets.sh
cd ../scripts/labtainer-student
smoketest.py

