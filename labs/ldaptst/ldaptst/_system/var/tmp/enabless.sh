#
#   Create self signed cert and enable SSL
#
./selfsign.sh
sed -i 's%^SLAPD_URLS.*$%SLAPD_URLS="ldapi:/// ldap:/// ldaps:///"%' /etc/sysconfig/slapd
systemctl restart slapd

