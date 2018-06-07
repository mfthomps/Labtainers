id | grep root >>/dev/null
result=$?
if [[ $result -eq 0 ]]; then
   df | grep lab_mnt >>/dev/null
   mounted=$?
   if [[ $mounted -ne 0 ]]; then
       sudo mount /dev/loop2 /lab_mnt
   fi
fi
