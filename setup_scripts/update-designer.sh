#!/bin/bash
#
# figure out where we are executing from and go to the labtainer directory
#
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
rm -f update-designer.sh
ln -s trunk/setup_scripts/update-designer.sh
full=`realpath trunk/setup_scripts/update-designer.sh`
ln -sf $full trunk/scripts/labtainer-student/bin/update-designer.sh
wget https://my.nps.edu/documents/107523844/109121513/labtainer-developer.tar/f377285e-23b5-4cd4-a578-c879b0200fff -O labtainer-developer.tar
cd ..
tar xf labtainer/labtainer-developer.tar
