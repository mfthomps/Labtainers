#!/bin/bash
#
#  Clone or pull latest SimLab
#
cd $LABTAINER_DIR
cd ../
echo "in $(pwd)"
if [[ ! -d Labtainers-simlab ]]; then
    echo "Labtainers-simlab does not exist, clone it"
    git clone https://gitlab.nps.edu/mfthomps/Labtainers-simlab.git
    ln -s Labtainers-simlab/simlab
    cd simlab
else
    cd simlab
    git pull
fi
