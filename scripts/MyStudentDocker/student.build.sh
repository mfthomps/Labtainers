#!/bin/bash

./buildImage.sh liveforensics analysis 
./buildImage.sh formatstring
./buildImage.sh bufoverflow
./buildImage.sh onewayhash
./buildImage.sh telnetlab client
./buildImage.sh telnetlab server
./buildImage.sh httplab client
./buildImage.sh httplab server
./buildImage.sh vpnlab client
./buildImage.sh vpnlab server
./buildImage.sh vpnlab router
