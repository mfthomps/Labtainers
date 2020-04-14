#!/bin/bash
if [[ ! -d Labtainers ]]; then
    git clone https://github.com/mfthomps/Labtainers.git
    cd Labtainers
else
    cd Labtainers
    git pull
fi
git checkout premaster
