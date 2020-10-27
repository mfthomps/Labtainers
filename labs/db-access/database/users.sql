# Creating accounts for remote hosts
CREATE user 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;

CREATE USER 'steven'@'executive' IDENTIFIED BY 'pass4steven';
GRANT ALL PRIVILEGES ON *.* TO 'steven'@'executive';

CREATE USER 'susan'@'hr' IDENTIFIED BY 'pass4susan';
GRANT ALL PRIVILEGES ON *.* TO 'susan'@'hr';

CREATE USER 'nancy'@'finance' IDENTIFIED BY 'pass4nancy';
GRANT ALL PRIVILEGES ON *.* TO 'nancy'@'finance';

CREATE USER 'david'@'it' IDENTIFIED BY 'pass4david';
GRANT ALL PRIVILEGES ON *.* TO 'david'@'it';

FLUSH PRIVILEGES;

