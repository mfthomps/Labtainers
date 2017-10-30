#!/bin/bash
read -p "This script will reboot the system when done, press enter to continue"
#
# ensure labtainer paths in .bashrc
#
target=~/.bashrc
grep ":./bin:" $target >>/dev/null
result=$?
if [[ result -ne 0 ]];then
   echo not in bashrc
   cat <<EOT >>$target
   if [[ ":$PATH:" != *":./bin:"* ]]; then 
       export PATH="${PATH}:./bin"
   fi
EOT
fi

ln -s trunk/scripts/labtainer-student
cd trunk/setup_scripts
found_distrib=`cat /etc/*-release | grep "^DISTRIB_ID" | awk -F "=" '{print $2}'`
if [[ -z "$1" ]]; then
    if [[ -z "$found_distrib" ]]; then
        # fedora gotta be different
        found_distrib=`cat /etc/*-release | grep "^NAME" | awk -F "=" '{print $2}'`
    fi 
    distrib=$found_distrib
else
    distrib=$1
fi
RESULT=0
case "$distrib" in
    Ubuntu)
        echo is ubuntu
        ./install-docker-ubuntu.sh
        RESULT=$?
        ;;
    Debian)
        echo is debian
        ./install-docker-debian.sh
        RESULT=$?
        ;;
    Fedora)
        echo is fedora
        ./install-docker-fedora.sh
        ;;
    Centos)
        echo is centos
        ./install-docker-centos.sh
        RESULT=$?
        ;;
    *)
        if [[ -z "$1" ]]; then
            echo "Did not recognize distribution: $found_distrib"
            echo "Try providing distribution as argument, either Ubuntu|Debian|Fedora|Centos"
        else
            echo $"Usage: $0 Ubuntu|Debian|Fedora|Centos"
        fi
        exit 1
esac
if [[ "$RESULT" -eq 0 ]]; then
    /usr/bin/newgrp docker <<EONG
    /usr/bin/newgrp $USER <<EONG
    docker pull mfthomps/labtainer.base
    docker pull mfthomps/labtainer.network
    docker pull mfthomps/labtainer.centos
EONG
    sudo reboot
else
    echo "There was a problem with the installation."
fi
