#!/bin/bash
#
# shrink a vmdk disk, first use 
#[cce_bash]
#sudo dd if=/dev/zero of=/emptyfile bs=1M
#sudo rm -rf /emptyfile
#[/cce_bash]
#
# to zero unused space
#
#VBoxManage modifymedium disk "/VMs/NewVirtualDisk1.vdi" --compact
VBoxManage modifymedium disk "$HOME/VirtualBox VMs/LabtainerVM24/LabtainerVM24.vdi" --compact
