#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
cd $HOME/ca
# root key generation
openssl genrsa -out private/ca.key.pem 4096
# self signed cert
openssl req -config openssl.cnf \
      -key private/ca.key.pem -nodes \
      -new -x509 -days 7300 -sha256 -extensions v3_ca \
      -subj '/CN=plc1.example.com/O=Example./C=US/ST=CA' \
      -out certs/ca.cert.pem

chmod 444 certs/ca.cert.pem

# intermediate key genteration
openssl genrsa -out intermediate/private/intermediate.key.pem 4096
chmod 400 intermediate/private/intermediate.key.pem

# cert signing request for intermediate cert
openssl req -config intermediate/openssl.cnf -new -sha256 \
      -key intermediate/private/intermediate.key.pem \
      -subj '/CN=plc1.example.com/O=Example./C=US/ST=CA' \
      -out intermediate/csr/intermediate.csr.pem

# sign the cert
openssl ca -batch -config openssl.cnf -extensions v3_intermediate_ca \
      -days 3650 -notext -md sha256 \
      -in intermediate/csr/intermediate.csr.pem \
      -out intermediate/certs/intermediate.cert.pem

chmod 444 intermediate/certs/intermediate.cert.pem

# create chain file
cat intermediate/certs/intermediate.cert.pem \
      certs/ca.cert.pem > intermediate/certs/ca-chain.cert.pem

# plc1 key gen
openssl genrsa -out intermediate/private/plc1.example.com.key.pem 2048
chmod 400 intermediate/private/plc1.example.com.key.pem

# plc1 cert signing request
openssl req -config intermediate/openssl.cnf \
      -key intermediate/private/plc1.example.com.key.pem \
      -subj '/CN=plc1.example.com/O=Example./C=US/ST=CA' \
      -new -sha256 -out intermediate/csr/plc1.example.com.csr.pem

# sign plc1 cert
openssl ca -batch -config intermediate/openssl.cnf \
      -extensions server_cert -days 375 -notext -md sha256 \
      -in intermediate/csr/plc1.example.com.csr.pem \
      -out intermediate/certs/plc1.example.com.cert.pem

chmod 444 intermediate/certs/plc1.example.com.cert.pem

# hmi1 key gen
openssl genrsa -out intermediate/private/hmi1.key.pem 2048
chmod 400 intermediate/private/hmi1.key.pem

# hmi1 cert signing request
openssl req -config intermediate/openssl.cnf \
      -key intermediate/private/hmi1.key.pem \
      -subj '/CN=hmi1/O=Example./C=US/ST=CA' \
      -new -sha256 -out intermediate/csr/hmi1.csr.pem

# sign hmi1 cert
openssl ca -batch -config intermediate/openssl.cnf \
      -days 375 -notext -md sha256 \
      -in intermediate/csr/hmi1.csr.pem \
      -out intermediate/certs/hmi1.cert.pem

chmod 444 intermediate/certs/hmi1.cert.pem

# give other boxes a chance to get their ssh going
# then copy keys/certs to appropriate boxes
sleep 3
sshpass -p password scp -o StrictHostKeyChecking=no intermediate/private/hmi1.key.pem hmi1:~/private/
sshpass -p password scp -o StrictHostKeyChecking=no intermediate/certs/ca-chain.cert.pem  intermediate/certs/hmi1.cert.pem hmi1:~/certs/

sshpass -p password scp -o StrictHostKeyChecking=no intermediate/private/plc1.example.com.key.pem plc1:~/private/
sshpass -p password scp -o StrictHostKeyChecking=no intermediate/certs/ca-chain.cert.pem  intermediate/certs/plc1.example.com.cert.pem plc1:~/certs/
#rm $HOME/.local/bin/fixlocal.sh
