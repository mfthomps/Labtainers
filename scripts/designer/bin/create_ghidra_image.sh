#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
END
source ./set_reg.sh
if [[ $LABTAINER_REGISTRY == "" ]]; then
   echo "No registry found"
   exit 1
fi
if [[ "$1" != -f ]]; then
   echo "This will build the labtainer $1 image.  "
   echo "Confirm that the dependent images have been published."
   echo "registry is $LABTAINER_REGISTRY"
   if [[ "$1" != -c ]]; then
       echo "This build will not use the docker cache, and may take a long time."
       echo "Use the -c option to speed things up."
   fi
   read -p "Continue? (y/n)"
   if [[ ! $REPLY =~ ^[Yy]$ ]]
   then
       echo exiting
       exit
   fi
else
   echo "registry is $LABTAINER_REGISTRY"
fi
CACHE="--no-cache"
if [[ "$1" == -c ]]; then
    CACHE=""
fi
here=`pwd`
mkdir /tmp/ghidra
echo "*****************do cp **"
cp ../base_dockerfiles/*ghidra /tmp/ghidra/
echo "DONE"
mkdir /tmp/ghidra/zip
cd /tmp/ghidra/zip
wget -N https://ghidra-sre.org/ghidra_9.1.1_PUBLIC_20191218.zip
wget -N https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.6%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz
wget -N https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.6%2B10/OpenJDK11U-jre_x64_linux_hotspot_11.0.6_10.tar.gz
wget -N https://corretto.aws/downloads/latest/amazon-corretto-11-x64-linux-jdk.tar.gz

cd ../
docker build $CACHE --build-arg registry=$LABTAINER_REGISTRY -f Dockerfile.labtainer.ghidra -t labtainer.ghidra:latest .


