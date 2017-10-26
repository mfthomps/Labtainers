#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
img_dir=/vfs
img_fid=/vfs/myfs.img
sudo mkdir $img_dir
sudo dd if=/dev/zero of=$img_fid bs=1k count=60k
#sudo mkfs.ext2 -F $img_fid
sudo mkfs -t ext2 -F $img_fid
sudo mkdir -p /lab_mnt
sudo mount -o loop $img_fid /lab_mnt
sudo chown student mnt
sudo mkdir /lab_mnt/usr
sudo cp -R /usr/bin /lab_mnt/usr/
cp /lab_mnt/usr/bin/who /lab_mnt/sur/bin/cheese
sudo umount mnt

