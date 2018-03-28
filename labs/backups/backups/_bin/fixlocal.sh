#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
#sudo cp /usr/bin/who /usr/bin/cheese
img_dir=/vfs
img_fid=/vfs/myfs.img
sudo mkdir $img_dir
sudo dd if=/dev/zero of=$img_fid bs=1k count=100k
sudo mkfs -t ext2 -F $img_fid
sudo mkdir -p /lab_mnt
sudo mount -o loop $img_fid /lab_mnt
sudo chown student mnt
sudo mkdir /lab_mnt/usr
sudo cp -R /usr/bin /lab_mnt/usr/
sudo cp /lab_mnt/usr/bin/who /lab_mnt/usr/bin/cheese
#sudo umount /lab_mnt

