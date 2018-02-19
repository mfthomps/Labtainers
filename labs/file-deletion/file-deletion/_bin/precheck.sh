#!/bin/bash
#
# Invoked prior to each command that is tracked,
# i.e., either local commands or those in treataslocal
#
# Create a file listing of the mnt directory
#
cd $HOME
sudo mount -o loop $HOME/myfs.img $HOME/mnt
sudo ls -l $HOME/mnt
sudo umount $HOME/mnt

