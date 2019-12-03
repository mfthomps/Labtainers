#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
# Create a disk image and make one partition on it.
# Then associate it with the next unused loopback device, create
# a file system on it, and mount it.  Then populate it with stuff.
#
chmod 0700 $HOME/.ssh
chmod 0600 $HOME/.ssh/id_rsa
sudo chmod 0700 root/.ssh
sudo chmod 0600 root/.ssh/id_rsa
img_dir=/vfs
img_fid=/vfs/myfs.img
sudo mkdir $img_dir
sudo dd if=/dev/zero of=$img_fid bs=1k count=100k
sudo parted -s /vfs/myfs.img mklabel bsd mkpart ext2 1 100
next=$(sudo losetup -f)
if [[ ! -b $next ]]; then
    # make the device if it does not exist (using mknod)
    count=${next:9}
    echo "count is $count"
    sudo mknod $next b 7 $count
fi
loopdev=$(sudo losetup -f /vfs/myfs.img -P --show)
sudo mkfs.ext2 $loopdev
sudo mkdir -p /lab_mnt
sudo mount $loopdev /lab_mnt
sudo mkdir /lab_mnt/usr
sudo cp -R /usr/bin /lab_mnt/usr/
sudo cp /lab_mnt/usr/bin/who /lab_mnt/usr/bin/cheese

