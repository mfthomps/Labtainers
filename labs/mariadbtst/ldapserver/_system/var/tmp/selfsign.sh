#!/bin/bash
#
# Create a self-signed cert for use with SSL
#
openssl req -new -x509 -nodes -out /etc/openldap/certs/exampleldap.crt -keyout /etc/openldap/certs/exampleldap.key -days 1460  -subj "/C=US/ST=Solid/L=Here/O=Example/CN=ldaptst.example.local"
chown -R ldap:ldap /etc/openldap/certs/example*
#
# OpenLDAP has a need to fail, which it will do on the first
# ldapmodify.  Folks on the web think order of key/cert matters, but it seems
# to be a matter of failing the first and then doing the other, then repeat
# the first.
#
ldapmodify -Y EXTERNAL  -H ldapi:/// -f xcert.ldif
ldapmodify -Y EXTERNAL  -H ldapi:/// -f xkey.ldif
ldapmodify -Y EXTERNAL  -H ldapi:/// -f xcert.ldif
