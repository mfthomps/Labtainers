#!/bin/bash
echo -e 'slapd slapd/internal/adminpw password adminpass' | debconf-set-selections
echo -e 'slapd slapd/internal/generated_adminpw password adminpass'| debconf-set-selections
echo -e 'slapd slapd/password2 password adminpass' | debconf-set-selections
echo -e 'slapd slapd/password1 password adminpass' | debconf-set-selections
echo -e 'slapd slapd/domain string example.com' |debconf-set-selections
echo -e 'slapd shared/organization string example' |debconf-set-selections
echo -e 'slapd slapd/backend string MDB' |debconf-set-selections
echo -e 'slapd slapd/purge_database boolean false' |debconf-set-selections
echo -e 'slapd slapd/move_old_database boolean true' |debconf-set-selections
echo -e 'slapd slapd/allow_ldap_v2 boolean false' |debconf-set-selections
echo -e 'slapd slapd/no_configuration boolean false' |debconf-set-selections

dpkg-reconfigure -fnointeractive slapd

