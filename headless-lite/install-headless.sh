
sudo apt-get install -y net-tools apt-transport-https ca-certificates curl software-properties-common
#curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
#sudo apt update
#sudo cache policy docker-ce
#sudo apt install -y docker-ce
curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose


adduser --disabled-password labtainer

sudo usermod -aG docker labtainer 
sudo usermod -aG sudo labtainer 

sudo mkdir /home/labtainer/headless-labtainers
sudo chown labtainer:labtainer /home/labtainer/headless-labtainers
sudo wget -P /home/labtainer/headless-labtainers https://raw.githubusercontent.com/mfthomps/Labtainers/premaster/headless-lite/headless-labtainers.sh
sudo chmod a+x /home/labtainer/headless-labtainers/headless-labtainers.sh
sudo systemctl enable headless-labtainers.service
sudo docker pull labtainers/labtainer.master.headless
