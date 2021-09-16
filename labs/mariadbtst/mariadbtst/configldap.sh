sudo authconfig --enableldap \
   --enableldapauth \
   --ldapserver="ldap://ldapserver" \
   --ldapbasedn="dc=example,dc=local" \
   --enablemkhomedir \
   --update
