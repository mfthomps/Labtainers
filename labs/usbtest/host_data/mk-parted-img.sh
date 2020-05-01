#!/bin/bash
img_fid=usb.img
dd if=/dev/zero of=$img_fid bs=1k count=100k
sudo parted $img_fid  mktable msdos
sudo parted $img_fid  mkpart p ext3 1 15
sudo parted $img_fid  mkpart p ext3 16 30

echo "Now run usb_create.sh and then use mkfs.ext3 or whatever on /dev/sdb1 and 2"
