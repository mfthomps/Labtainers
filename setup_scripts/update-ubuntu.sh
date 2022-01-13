if [ ! -d "$HOME/headless-labtainers" ]; then
    if [ $USER == student ]; then
        echo -e password123 | sudo -S DEBIAN_FRONTEND=noninteractive apt-get -y install containerd
    else
        sudo apt-get -y install containerd
    fi
fi
haspip3=$(dpkg -l python3-pip)
if [ -z "$haspip3" ]; then
    echo "Need to install python3-pip package, will sudo apt-get"
    # broken linux update garbage
    echo -e password123 | sudo -S rm -f /var/lib/dpkg/lock
    if [ $USER == student ]; then
        echo -e password123 | sudo -S apt-get update
        echo -e password123 | sudo -S apt-get install -y python3-pip
    else
        sudo apt-get update
        sudo apt-get install -y python3-pip
    fi
fi
hasdocker=$(pip3 list --format=legacy | grep docker)
if [ -z "$hasdocker" ]; then
    echo "Need to install docker python module, will sudo pip3"
    if [ $USER == student ]; then
       echo -e password123 | sudo -S pip3 install docker
    else
       sudo pip3 install docker
    fi
fi
