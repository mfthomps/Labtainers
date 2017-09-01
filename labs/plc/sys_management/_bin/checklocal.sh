!/usr/bin/env bash

# checklocal.sh
# Description:
#     This file should contain checks for local settings (such as sysctl)
#     specific for each lab.  The resulting output will go into the
#     checklocal.stdout.timestamp file
#
MANAGEHASH="manage_plc.py "$(openssl dgst -md5 "manage_plc.py")
echo $MANAGEHASH
PLCHASH="plc.c "$(openssl dgst -md5 "plc.c")
echo $PLCHASH
HIDDENFILEHASH="nothere "$(tar -cf - .nothere | md5sum | openssl dgst -md5)
echo $HIDDENFILEHASH
