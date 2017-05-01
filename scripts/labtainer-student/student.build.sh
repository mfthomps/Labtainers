#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
END

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
