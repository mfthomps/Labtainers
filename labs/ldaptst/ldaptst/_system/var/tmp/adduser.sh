ldapadd -x -w password -D "cn=ldapadm,dc=example,dc=local" -f projx.ldif
ldapadd -x -w password -D "cn=ldapadm,dc=example,dc=local" -f mike.ldif
ldappasswd -s mikepassword -w password -D "cn=ldapadm,dc=example,dc=local" -x "uid=mike,ou=People,dc=example,dc=local"
