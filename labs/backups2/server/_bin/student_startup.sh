id | grep root >>/dev/null
result=$?
if [[ $result -eq 0 ]]; then
# 
#  Mount the loopback device on /lab_mnt if not already mounted.
#  Need to first find which loopback device is mapped to /vfs/myfs.img.
#  Take most recent one, there may be many.
#
   df | grep lab_mnt >>/dev/null
   mounted=$?
   if [[ $mounted -ne 0 ]]; then
       loopdev=$(losetup -l | grep /vfs/myfs.img | head -1 | awk '{print $1}')
       sudo mount $loopdev /lab_mnt
   fi
fi
