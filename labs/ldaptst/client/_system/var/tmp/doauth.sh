#!/bin/bash
#
# Enable ldap and define server address.  Intitially do not use SSL
#
authconfig --enableldap --enableldapauth --ldapserver=192.0.0.2 --ldapbasedn="dc=example,dc=local" --enablemkhomedir --update
systemctl restart nslcd

