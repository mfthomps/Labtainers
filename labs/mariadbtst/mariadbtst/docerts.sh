cdir=/etc/my.cnf.d/certificates
mkdir -p $cdir
openssl genrsa 2048 >$cdir/ca-key.pem
openssl req -new -x509 -nodes -days 356000 -key $cdir/ca-key.pem -subj "/C=US/ST=Solid/L=Here/O=Example/CN=ca.example.local" -out $cdir/ca.pem
openssl req -newkey rsa:2048 -days 465000 -nodes -keyout $cdir/server-key.pem -subj "/C=US/ST=Solid/L=Here/O=Example/CN=mariadbtst" -out $cdir/server-req.pem
openssl rsa -in $cdir/server-key.pem -out $cdir/server-key.pem

openssl x509 -req -in $cdir/server-req.pem -days 365000 -CA $cdir/ca.pem -CAkey $cdir/ca-key.pem -set_serial 01 -out $cdir/server-cert.pem
chown mysql:mysql $cdir/*
