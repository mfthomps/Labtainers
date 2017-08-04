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
#
# Install Docker on an Ubuntu system, along with other packages required by Labtainers
#
read -p "This script will reboot the system when done, press enter to continue"

#---needed packages for install
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common 

#---adds docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - 

#---sets up stable repository
sudo apt-get update
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

#---installs Docker: Community Edition
sudo apt-get update
sudo apt-get -y install docker-ce 

#---starts and enables docker
sudo systemctl start docker
sudo systemctl enable docker

#---gives user docker commands
sudo groupadd docker
sudo usermod -aG docker $USER 

#---other packages required by Labtainers
sudo apt-get -y install python-pip 
sudo -H pip install --upgrade pip
sudo -H pip install netaddr
sudo apt-get -y install openssh-server

#---Checking if packages have been installed. If not, the system will not reboot and allow the user to investigate.
declare -a packagelist=("apt-transport-https" "ca-certificates" "curl" "software-properties-common" "docker-ce" "python-pip" "openssh-server")
packagefail="false"

for i in "${packagelist[@]}"
do
#echo $i
packagecheck=$(dpkg -s $i 2> /dev/null | grep Status)
#echo $packagecheck
    if [ "$packagecheck" != "Status: install ok installed" ]; then
       if [ $i = docker-ce ];then 
           echo "ERROR: '$i' package did not install properly. Please check the terminal output above for any errors related to the pacakge installation. If the issue persists, go to docker docs and follow the instructions for installing docker. (Make sure the instructions is CE and is for your Linux distribution,e.g., Ubuntu and Fedora.)"
       else
           echo "ERROR: '$i' package did not install properly. Please check the terminal output above for any errors related to the pacakge installation. Try installing the '$i' package individually by executing this in the command line: 'sudo apt-get install $i" 
       fi 
       packagefail="true"
       #echo $packagefail
    fi
done

pipcheck=$(pip list 2> /dev/null | grep -F netaddr)
#echo $pipcheck
if [ -z "$pipcheck" ]; then
    echo "ERROR: 'netaddr' package did not install properly. Please check the terminal output for any errors related to the pacakge installation. Make sure 'python-pip' is installed and then try running this command: 'sudo -H pip install netaddr' "
    packagefail="true"
    #echo $packagefail
fi

#
#Add the hosts DNS servers to the /etc/resolv.conf by appending them
#to the resolv.conf.d/head file.  Dockers on ubuntu, cannot resolve
#addresses from within containers.
#
dns_list=$(nmcli dev show | grep DNS | awk '{print $2 $4}')
echo already is $dns_list
for dns in $dns_list
do
    already=$(grep $dns /etc/resolvconf/resolv.conf.d/head)
    if [ -z "$already" ]; then
        echo "nameserver $dns" | sudo tee -a /etc/resolvconf/resolv.conf.d/head
    fi
done
sudo resolvconf -u

if [ $packagefail = "true" ]; then
    echo "If you manually install packages to correct the problem, be sure to reboot the system before trying to use Labtainers."
    exit
fi

sudo reboot

#Notes: The “-y” after each install means that the user doesn’t need to press “y” in between each package download. The install script is based on this page: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/
