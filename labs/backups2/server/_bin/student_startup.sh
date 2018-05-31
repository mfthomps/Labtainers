id | grep root >>/dev/null
result=$?
if [[ $result -eq 0 ]]; then
   df | grep lab_mnt >>/dev/null
   mounted=$?
   if [[ $mounted -ne 0 ]]; then
       img_fid=/vfs/myfs.img
       sudo mount -o loop $img_fid /lab_mnt
   fi
fi
