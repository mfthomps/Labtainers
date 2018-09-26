#!/bin/bash
#
#  This script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument,
#  (the user ID is the second parameter)
#  If this script is to use sudo and the sudoers for the lab
#  does not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
#  If you issue commands herein to start services, and those services
#  have unit files prescribing their being started after the
#  waitparam.service, then first create the flag directory that
#  waitparam sleeps on:
#
#   PERMLOCKDIR=/var/labtainer/did_param
#   echo $1 | sudo -S mkdir -p "$PERMLOCKDIR"
cd $HOME
#export WINEDLLOVERRIDES="mscoree,mshtml="
#wine msiexec /i /var/tmp/wine-mono-4.7.1.msi
#export WINEDLLOVERRIDES=""
echo "Now install CyberCIEGE"
wine /var/tmp/setup1-9v8s.exe
mv $HOME/gstart.exe $HOME/.wine/drive_c/
wine regedit $HOME/linuxnative.reg
mkdir -p "$HOME/.wine/drive_c/users/$USER/Application Data/CyberCIEGE"
ln -s "$HOME/.wine/drive_c/Program Files (x86)/CyberCIEGE/game/exec/encylo" "$HOME/.wine/drive_c/users/$USER/Application Data/CyberCIEGE/encylo"
