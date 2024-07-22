#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
END
#
# Install Docker on an Ubuntu system, along with other packages required by Labtainers
#

#Check if current user is user login. (Targeted to avoid adding root user into docker group instead of the the user logged in account.)
currUser=`who | head -n1 | awk '{print $1}'`
if [ "$USER" != "$currUser" ]; then
    echo "You are not the login user. If you are root user, please exit. And run this script again."
    exit
fi

type sudo >/dev/null 2>&1 || { echo >&2 "Please install sudo.  Aborting."; exit 1; }
sudo -v || { echo >&2 "Please make sure user is sudoer.  Aborting."; exit 1; }
#---needed packages for install
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common  xterm
RESULT=$?
if [ $RESULT -ne 0 ];then
    echo "problem fetching packages, exit"
    exit 1
fi
version=$(lsb_release -a | grep Release: | cut -f 2)
docker_package=docker-ce
#---adds docker<92>s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

#---sets up stable repository
sudo apt-get update
sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

#---installs Docker: Community Edition
sudo apt-get update
sudo apt-get -y install docker-ce

#---starts and enables docker
sudo systemctl start docker
sudo systemctl enable docker

#---gives user docker commands
sudo groupadd docker
sudo usermod -aG docker $USER 

#---Use virtual python environment to avoid Ubuntu lockdown
sudo apt -y install python3.12-venv
sudo mkdir -p /opt/labtainer/venv
sudo python3 -m venv /opt/labtainer/venv
#-- downgrade requests and urllib packages due to docker python module bug
sudo /opt/labtainer/venv/bin/python3 -m pip install 'requests<2.29.0' 'urllib3<2.0' || exit 1
sudo /opt/labtainer/venv/bin/python3 -m pip install netaddr parse python-dateutil docker || exit 1

#---other packages required by Labtainers
sudo apt-get -y install openssh-server || exit 1
echo 'source $LABTAINER_DIR/setup_scripts/lab-completion.bash' >> /home/$USER/.bashrc
#---Allow use of VM's systemd by containers
sudo sed -i 's/"quiet splash"/"quiet splash systemd.unified_cgroup_hierarchy=0"/' /etc/default/grub
sudo update-grub

exit 0

