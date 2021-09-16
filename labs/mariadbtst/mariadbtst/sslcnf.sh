#!/bin/bash
sed -i '/^.mariadb/a ssl_cert = /etc/my.cnf.d/certificates/server-cert.pem\n\
ssl_key = /etc/my.cnf.d/certificates/server-key.pem\n\
ssl_ca = /etc/my.cnf.d/certificates/ca.pem' /etc/my.cnf.d/server.cnf
systemctl restart mariadb
