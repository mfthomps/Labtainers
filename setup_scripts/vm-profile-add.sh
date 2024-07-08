#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

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
#  DO NOT select "custom" install, it is not really, and it will break the clock and will fail to installvmware tools.
#  May have to manually set time and then install open-vm-tools-desktop
#  DO NOT allow updates, do not do an update from ubuntu 18.  VMWare will fail to 
#  boot the updated VM 9/10 times.
# set automatic login: activities / users / unlock / automatic login
# hw compatability to old version  VM / Manage / Change HW compatabilityh  ws 14?
# ALL
# add terminal to desktop
# bidirectional shared clipboard
# sudo apt-get install net-tools
# wget --quiet https://github.com/mfthomps/Labtainers/releases/latest/download/labtainer.tar -O labtainer.tar
# tar xf labtainer.tar
# rm labtainer.tar
# cd labtainer
# ./install-labtainer.sh
# reboot
# setup-scripts/vm-profile-add.sh
#
# remove snapd and its /var/cache
#
echo "rm -f \$HOME/labtainer/.did_message" >> ~/.profile
echo "export PATH=\${PATH}:./bin" >> ~/.profile

mkdir -p $HOME/.config/autostart
cp $HOME/labtainer/trunk/setup_scripts/gnome-terminal.desktop $HOME/.config/autostart/
touch $HOME/labtainer/.doupdate 

target=$HOME/.bashrc
cat <<EOT >>$target
   if [ -f $HOME/labtainer/.doupdate ]; then
       rm -f \$HOME/labtainer/.doupdate
       \$HOME/labtainer/update-labtainer.sh
   fi
   if [ ! -f \$HOME/labtainer/.did_message ]; then
       clear
       cat README
       touch \$HOME/labtainer/.did_message
   fi
EOT


#gsettings set org.gnome.settings-daemon.plugins.power power-button-action 'shutdown'
# shutdown no longer supported.  ubuntu has become a nanny.
gsettings set org.gnome.settings-daemon.plugins.power power-button-action 'suspend'
gsettings set org.gnome.nm-applet disable-disconnected-notifications "true"
gsettings set org.gnome.nm-applet disable-connected-notifications "true"
gsettings set org.gnome.desktop.session idle-delay 0
gsettings set org.gnome.desktop.screensaver lock-enabled false

mkdir -p $HOME/labtainer_xfer
cd $HOME/Desktop
ln -s $HOME/labtainer/trunk/docs/student/labtainer-student.pdf
ln -s ~/labtainer_xfer
# xdotool does not work with wayland
sudo sed -i s/^.WaylandEnable=false/WaylandEnable=false/ /etc/gdm3/custom.conf
dconf load /org/gnome/terminal/legacy/profiles:/ < $HOME/labtainer/trunk/config/gnome-terminal-profiles.dconf

