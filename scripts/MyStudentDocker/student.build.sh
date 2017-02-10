#!/bin/bash

./buildImage.sh liveforensics 
./buildImage.sh formatstring
./buildImage.sh bufoverflow
./buildImage.sh onewayhash
./buildImage.sh telnetlab client
./buildImage.sh telnetlab server
