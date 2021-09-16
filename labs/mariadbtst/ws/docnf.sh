mkdir -p /etc/mysql/mariadb.conf.d/certificates
sshpass -p "ubuntu" scp -o 'StrictHostKeyChecking no' ubuntu@mariadbtst:/etc/my.cnf.d/certificates/ca.pem /tmp/
cp /tmp/ca.pem /etc/mysql/mariadb.conf.d/certificates/
sed -i '/^.client-mariadb/a ssl_ca = /etc/mysql/mariadb.conf.d/certificates/ca.pem\nssl-verify-server-cert' /etc/mysql/mariadb.conf.d/50-client.cnf
