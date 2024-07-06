# msc ubuntu breakage
echo -e password123 | sudo -S rm /var/lib/dpkg/lock
echo -e password123 | sudo -S apt-get update
echo -e password123 | sudo -S rm /var/lib/dpkg/lock
echo -e password123 | sudo -S apt-get install --reinstall libappstream4
echo -e password123 | sudo -S apt-get update
if [ ! -d "$HOME/headless-labtainers" ]; then
    if [ $USER == student ]; then
        echo -e password123 | sudo -S DEBIAN_FRONTEND=noninteractive apt-get -y install containerd
    else
        sudo apt-get -y install containerd
    fi
fi
#---Use virtual python environment to avoid Ubuntu lockdown
if [ ! -d /opt/labtainer/venv/bin ]; then
    haspip3=$(dpkg -l python3-pip)
    if [ -z "$haspip3" ]; then
        echo "Need to install python3-pip package, will sudo apt-get"
        # broken linux update garbage
        echo -e password123 | sudo -S rm -f /var/lib/dpkg/lock
        if [ $USER == student ]; then
            echo -e password123 | sudo -S apt-get install -y python3-pip
        else
            sudo apt-get update
            sudo apt-get install -y python3-pip
        fi
    fi
    sudo apt -y install python3-venv
    sudo mkdir -p /opt/labtainer/venv
    sudo python3 -m venv /opt/labtainer/venv
    sudo ln -s /opt/labtainer/venv/bin/python /opt/labtainer/python3
    #-- downgrade requests and urllib packages due to docker python module bug
    sudo /opt/labtainer/venv/bin/python3 -m pip install 'requests<2.29.0' 'urllib3<2.0' || exit 1
    sudo /opt/labtainer/venv/bin/python3 -m pip install netaddr parse python-dateutil docker || exit 1
fi
