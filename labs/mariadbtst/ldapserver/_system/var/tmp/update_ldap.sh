ldapmodify -Y EXTERNAL  -H ldapi:/// -f db.ldif
ldapmodify -Y EXTERNAL  -H ldapi:/// -f monitor.ldif
cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG
chown ldap:ldap /var/lib/ldap/*
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/cosine.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/nis.ldif 
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/inetorgperson.ldif


ldapadd -x -w password -D "cn=ldapadm,dc=example,dc=local" -f base.ldif
#ldapadd -x -w password -D "cn=ldapadm,dc=example,dc=local" -f monitor.ldif
