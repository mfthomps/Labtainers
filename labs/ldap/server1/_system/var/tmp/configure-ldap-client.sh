#!/bin/bash
# hacked reconfiguration of ldap-auth-config
export VISUAL=/var/tmp/install-ldap-auth-config.sh
dpkg-reconfigure -feditor ldap-auth-config
# causes first password change to fail.  
sed -i 's/use_authtok//'  /etc/pam.d/common-password

# enable use of ldap for authentication
sudo sed -i 's/^passwd:.*/passwd:    compat ldap/' /etc/nsswitch.conf
sudo sed -i 's/^group:.*/group:    compat ldap/' /etc/nsswitch.conf
sudo sed -i 's/^shadow:.*/shadow:    compat ldap/' /etc/nsswitch.conf
sudo sed -i 's/^gshadow:.*/gshadow:    compat ldap/' /etc/nsswitch.conf


sudo sed -i '/and here are more per-package modules/a session required        pam_mkhomedir.so umask=0022 skel=/etc/skel' /etc/pam.d/common-session
sudo sed -i '/pam_systemd.so/d' /etc/pam.d/common-session
sudo sed -i 's/session optional.* pam_ldap.so/session required  pam_ldap.so/' /etc/pam.d/common-session
sudo sed -i 's/.*pam_ldap.so.*/session required  pam_ldap.so/' /etc/pam.d/common-session

systemctl restart nscd
