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
rm -f update-labtainer.sh
ln -s trunk/setup_scripts/update-labtainer.sh
full=`realpath trunk/setup_scripts/update-labtainer.sh`
ln -sf $full trunk/scripts/labtainer-student/bin/update-labtainer.sh

if [[ -z "$LABTAINER_TESTING" ]]; then
    wget https://my.nps.edu/documents/107523844/109121513/labtainer.tar/6fc80410-e87d-4e47-ae24-cbb60c7619fa -O labtainer.tar
fi
cd ..
tar xf labtainer/labtainer.tar
labtainer/trunk/setup_scripts/pull-all.sh
#
# ensure labtainer paths in .bashrc
#
target=~/.bashrc
grep ":./bin:" $target >>/dev/null
result=$?
if [[ result -ne 0 ]];then
   cat <<EOT >>$target
   if [[ ":\$PATH:" != *":./bin:"* ]]; then 
       export PATH="\${PATH}:./bin"
   fi
EOT
fi
