#!/bin/bash
#
# Modify the user profile to create a terminal on login that
# starts in the labtainer workspace.  The profile will also, run the Labtainer
# update script if the labtainer/.doupdate file exists.
# This script also creates the .doupdate file and modifieds gnmoe
# to shutdown when the virtual powerbutton is pressed.
#
cat >>~/.profile <<EOL
gnome-terminal --geometry 120x31+150+300 --working-directory=/home/student/labtainer/labtainer-student -e "bash -c \"/bin/cat README; exec bash\"" &
if [[ -f /home/student/labtainer/.doupdate ]]; then
    gnome-terminal --geometry 73x31+100+300 --working-directory=/home/student/labtainer -x ./update-labtainer.sh
fi
EOL
touch /home/student/labtainer/.doupdate 
gsettings set org.gnome.settings-daemon.plugins.power button-power 'shutdown'
