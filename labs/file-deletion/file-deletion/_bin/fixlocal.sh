#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
cd $HOME
dd if=/dev/zero of=myfs.img bs=1k count=1k
mkfs.ext2 -F myfs.img
sudo mount -o loop myfs.img mnt
sudo chown student mnt
for i in `seq 0 RND_MAX`; do
    fname="mnt/fillerfile"
    fname+=$i
    echo “dumb filler” > fname
done
echo “First file created” > mnt/file1
echo “Second file created” > mnt/file2
echo “Third file” > mnt/file3
sudo umount mnt

dd if=/dev/zero bs=1024 count=2048 of=ntfs.img
mkntfs -F ntfs.img
sudo mount -o loop ntfs.img mnt
sudo chown student mnt
echo “First file created” > mnt/file1
echo “Second file created” > mnt/file2
echo “Third file” > mnt/file3
sudo umount mnt
