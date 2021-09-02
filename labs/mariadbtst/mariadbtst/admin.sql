# Creating accounts for remote hosts
CREATE user 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;

INSTALL SONAME 'auth_pam';
CREATE USER 'mike'@'localhost' IDENTIFIED VIA pam USING 'mysql';

CREATE DATABASE dumb;
GRANT ALL ON dumb.* TO 'mike'@'localhost';

