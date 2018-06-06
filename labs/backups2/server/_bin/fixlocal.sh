#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
img_dir=/vfs
img_fid=/vfs/myfs.img
sudo mkdir $img_dir
sudo dd if=/dev/zero of=$img_fid bs=1k count=100k
sudo parted -s /vfs/myfs.img mklabel bsd mkpart ext2 1 100
sudo losetup -f /vfs/myfs.img -P --show
sudo mkfs.ext2 /dev/loop2
sudo mkdir -p /lab_mnt
sudo mount /dev/loop2 /lab_mnt
sudo mkdir /lab_mnt/usr
sudo cp -R /usr/bin /lab_mnt/usr/
sudo cp /lab_mnt/usr/bin/who /lab_mnt/usr/bin/cheese

