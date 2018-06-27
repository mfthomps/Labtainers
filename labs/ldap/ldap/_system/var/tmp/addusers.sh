ldapadd -x -w adminpass -D "cn=admin,dc=example,dc=com" -f /var/tmp/base.ldif
ldapadd -x -w adminpass -D "cn=admin,dc=example,dc=com" -f $HOME/projx.ldif
ldapadd -x -w adminpass -D "cn=admin,dc=example,dc=com" -f $HOME/mike.ldif
ldappasswd -s password123 -w adminpass -D "cn=admin,dc=example,dc=com" -x "uid=mike,ou=users,dc=example,dc=com"
