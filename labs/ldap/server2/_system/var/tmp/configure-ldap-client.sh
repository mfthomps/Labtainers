#!/bin/bash
# hacked reconfiguration of ldap-auth-config
export VISUAL=/var/tmp/install-ldap-auth-config.sh
dpkg-reconfigure -feditor ldap-auth-config
# causes first password change to fail.  
sed -i 's/use_authtok//'  /etc/pam.d/common-password

# enable use of ldap for authentication
sudo sed -i 's/compat/compat ldap/' /etc/nsswitch.conf

sudo sed -i '/and here are more per-package modules/a session required        pam_mkhomedir.so umask=0022 skel=/etc/skel' /etc/pam.d/common-session

systemctl restart nscd
