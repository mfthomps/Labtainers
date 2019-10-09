#s!/bin/bash
#
# Modify the user profile to create a terminal on login that
# starts in the labtainer workspace.  The profile will also, run the Labtainer
# update script if the labtainer/.doupdate file exists.
# This script also creates the .doupdate file and modifieds gnome
# to shutdown when the virtual powerbutton is pressed.
#
# Create new Ubuntu VM 40GB 4 GB RAM; 2 CPUs; VMSVGA; 3d accelleration
# disable auto upgrades in /etc/apt/apt.conf.d/20auto-upgrades
# comment out /etc/apt/apt.conf.d/99update-notifier

# VBOX:
# sudo apt install build-essential dkms linux-headers-$(uname -r)
# install guest additions
#sudo usermod -G vboxsf -a $USER
# VMWARE:
# set automatic login: activities / users / unlock / automatic login
# ALL
# add terminal to desktop
# bidirectional shared clipboard
# wget https://my.nps.edu/documents/107523844/109121513/labtainer.tar
# tar xf labtainer.tar
# rm labtainer.tar
# cd labtainer
# ./install-labtainer.sh
# reboot
# setup-scripts/vm-profile-add.sh

#
# clone (as linked) a smoketest box
# remove .doupdate
# echo "frank@beans.com" > $HOME/.local/share/labtainers/email.txt
# add $HOME/labtainer/trunk/testsets/bin to path in bashrc
# visudo and change sudo etnry to: ALL=(ALL) NOPASSWD:ALL
# apt-get install xdotool
# apt-get install vim
# setup-scripts/prep-testregistry.sh
# touch $HOME/labtainer/.dosmoke
#
cat >>~/.profile <<EOL
gnome-terminal --geometry 120x31+150+300 --working-directory=$HOME/labtainer/labtainer-student -e "bash -c \"/bin/cat README; exec bash\"" &
if [[ -f $HOME/labtainer/.doupdate ]]; then
    gnome-terminal --geometry 73x31+100+300 --working-directory=$HOME/labtainer -x ./update-labtainer.sh
fi
if [[ -f $HOME/labtainer/.dosmoke ]]; then
    gnome-terminal --geometry 120x31+150+300 --working-directory=$HOME/labtainer/trunk/setup_scripts -e "bash -c \"exec bash -c ./full-smoke-test.sh \"" &
fi

EOL
touch $HOME/labtainer/.doupdate 
gsettings set org.gnome.settings-daemon.plugins.power button-power 'shutdown'
gsettings set org.gnome.nm-applet disable-disconnected-notifications "true"
gsettings set org.gnome.nm-applet disable-connected-notifications "true"
gsettings set org.gnome.desktop.session idle-delay 0
gsettings set org.gnome.desktop.screensaver lock-enabled false

mkdir -p $HOME/labtainer_xfer
cd $HOME/Desktop
ln -s $HOME/labtainer/trunk/docs/student/labtainer-student.pdf
ln -s ~/labtainer_xfer


