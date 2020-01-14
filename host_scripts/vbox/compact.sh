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
#vmware-vdiskmanager -k "~/VirtualBox\ VMs/LabtainerVM-2/*vmdk"
VBoxManage modifymedium disk "/VMs/NewVirtualDisk1.vdi" --compact
