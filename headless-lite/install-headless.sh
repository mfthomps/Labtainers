#!/bin/bash
#
# This assumes user 1000 is labtainer
#
TEST_FLAG=""
if [[ "$1" == "-t" ]]; then
    echo "TEST_FLAG set to -t" 
    TEST_FLAG=-t
fi
apt-get install -y net-tools apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
apt update
cache policy docker-ce
apt install -y docker-ce
curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose


mkdir /home/labtainer/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCqsA7lR0ks4PhVZ7P2vqormMrYlq/P4UeIrnvpgITd//o/x6W0l7Q6oOsp/bBJudB/91ZxTY7yTuXlSRIAg04SC4Fy/jpvz3Uh+Z8o/dfsd4Agoq0hOmm+UU1tC+hHQq1rwocYc2dnf79fyVa9xcL9xTKOjNNLLT7M6wwv+cTSBD+ivc40bMrt5lez/mldefu4Jsy1Z+bWNkg6BIY1LAzZ86EzcWZN7KHYzsKziNq8M8e4pDtG5a3QGf8HCUrEgCx8cbA6oNA2har2t/sALDtcEMzG/OhiBS2FopxC8aLZtAp29PPIOv5Z+S/w0NcQZnoNSXcNk+TNwOO2qZ+r0GbK/4s9LQrix0o0WfETqccBbb0KTqgTJEAzBqDITMQmG6qucU5yN0yWKPO+4CtndSp2GObnGU+LlRx8VYmacAqyn2tA1sV1bXzZJQ4nRuhbqLPDwRdMSslEiDz/5fkQEho/RLd8EuU+qGA39UgBvaNCV24Y4nYsojXcewvcTqY4T/0= mfthomps@mac-0220" > /home/labtainer/.ssh/authorized_keys
chown labtainer:labtainer /home/labtainer/.ssh/authorized_keys

groupadd docker
usermod -aG docker labtainer 
usermod -aG sudo labtainer 

mkdir -p /home/labtainer/headless-labtainers
chown labtainer:labtainer /home/labtainer/headless-labtainers
wget -P /home/labtainer/headless-labtainers https://raw.githubusercontent.com/mfthomps/Labtainers/premaster/headless-lite/headless-labtainers.sh
chmod a+x /home/labtainer/headless-labtainers/headless-labtainers.sh
tee -a /lib/systemd/system/headless-labtainers.service > /dev/null <<EOT
   [Unit]
   Description=Headless Labtainers

   [Service]
   Type=simple
   WorkingDirectory=/home/labtainer/headless-labtainers
   User=labtainer
   ExecStart=/home/labtainer/headless-labtainers/headless-labtainers.sh $TEST_FLAG

   [Install]
   WantedBy=multi-user.target
   Alias=headless-labtainers.service
EOT
echo "%sudo ALL=(ALL) NOPASSWD:ALL" >>/etc/sudoers

if [[ -z "$TEST_FLAG" ]]; then
    docker pull labtainers/labtainer.master.headless
    docker pull accetto/ubuntu-vnc-xfce
else
    wget -P /home/labtainer/headless-labtainers https://raw.githubusercontent.com/mfthomps/Labtainers/premaster/setup_scripts/prep-testregistry.sh
    wget -P /home/labtainer/headless-labtainers https://raw.githubusercontent.com/mfthomps/Labtainers/premaster/setup_scripts/testreg-add.py
    cd /home/labtainer/headless-labtainers
    chmod a+x prep-testregistry.sh testreg-add.py
    ./prep-testregistry.sh
    docker pull testregistry:5000/labtainer.headless.tester
    echo "Pulled tester" >>/tmp/headless.log
    docker pull testregistry:5000/ubuntu-vnc-xfce
fi

systemctl enable headless-labtainers.service
systemctl start headless-labtainers.service
chown root:docker /var/run/docker.sock
