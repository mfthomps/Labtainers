#
#   Create self signed cert and enable SSL
#
./selfsign.sh
sed -i 's%^SLAPD_SERVICES.*$%SLAPD_SERVICES="ldapi:/// ldap:/// ldaps:///"%' /etc/default/slapd
systemctl restart slapd

