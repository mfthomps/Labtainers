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
#
# figure out where we are executing from and go to the labtainer directory
#
if [ "$#" -eq 1 ]; then
   if [ "$1" == "-t" ]; then
       export TEST_REGISTRY=TRUE
   else
       echo "update-labtainers [-t]"
       echo "   use -t to pull tar from /media/sf_SEED"
       echo "   and pull images from the test registry"
       exit
   fi
elif [ "$#" -ne 0 ]; then
   echo "update-labtainers [-t]"
   echo "   use -t to pull tar from /media/sf_SEED"
   echo "   and pull images from the test registry"
   exit
fi
here=`pwd`
if [[ $here == */labtainer ]]; then
   echo is at top >> /dev/null
elif [[ $here == */labtainer-student ]]; then
   #echo is in student
   real=`realpath ./`
   cd $real
   cd ../../..
elif [[ $here == */setup_scripts ]]; then
   cd ../../
else
   echo "Please run this script from the labtainer or labtainer-student directory"
   exit
fi
labtainer_root=`pwd`
target=~/.bashrc
grep ":scripts/designer/bin:" $target | grep PATH >>/dev/null
result=$?
if [[ result -ne 0 ]];then
   cat <<EOT >>$target
   if [[ ":\$PATH:" != *":scripts/designer/bin:"* ]]; then 
       export PATH="\${PATH}:$labtainer_root/trunk/scripts/designer/bin"
       export LABTAINER_DIR=$labtainer_root/trunk
   fi
EOT
fi
rm -f update-designer.sh
ln -s trunk/setup_scripts/update-designer.sh
full=`realpath trunk/setup_scripts/update-designer.sh`
HOSTNAME=`hostname`
ln -sf $full trunk/scripts/labtainer-student/bin/update-designer.sh
if [[ "$TEST_REGISTRY" != TRUE ]]; then
    #wget https://my.nps.edu/documents/107523844/109121513/labtainer-developer.tar/f377285e-23b5-4cd4-a578-c879b0200fff -O labtainer-developer.tar
    wget --quiet https://nps.box.com/shared/static/xk9e07r7m5szrc9owggawyxzy5w3rzrh.tar -O labtainer-developer.tar
else
    cp /media/sf_SEED/test_vms/$HOSTNAME/labtainer-developer.tar .
    echo "USING SHARED FILE TAR, NOT PULLING FROM WEB"
fi
if [[ "$TEST_REGISTRY" != TRUE ]]; then
   sudo trunk/setup_scripts/dns-add.py
   sudo systemctl restart docker
fi
#sudo -H pip install netaddr parse python-dateutil
cd ..
# ad-hoc clean up.  remove after a while
rm -f labtainer/trunk/scripts/labtainer-student/bin/SimLab*

tar xf labtainer/labtainer-developer.tar
grep "^Distribution created:" labtainer/trunk/README.md | awk '{print "Updated to release of: ", $3, $4}'

if [ ! -L $HOME/Desktop/labdesigner.pdf ]; then
       ln -s "$(pwd)"/labtainer/trunk/docs/labdesigner/labdesigner.pdf $HOME/Desktop/labdesigner.pdf
fi
