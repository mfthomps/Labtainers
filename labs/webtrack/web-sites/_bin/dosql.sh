#!/bin/bash
while [ 1 ]; do
    date
    mysql -u root -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('seedubuntu')"
    result=$?
    if [[ $result == 0 ]]; then
        break
    else
        echo no server, sleep
        sleep 1
    fi
done
mysql -u root -pseedubuntu -e "CREATE DATABASE if not exists myelgg; "
mysql -u root -pseedubuntu myelgg < $HOME/myelgg.sql
mysql -u root -pseedubuntu -e "CREATE DATABASE if not exists revive_adserver; "
mysql -u root -pseedubuntu revive_adserver < $HOME/revive.sql
mysql -u root -pseedubuntu -e "CREATE USER 'wtuser'@'localhost' IDENTIFIED BY 'seeduser';"
mysql -u root -pseedubuntu -e "GRANT ALL PRIVILEGES ON revive_adserver.* TO 'wtuser'@'localhost';"
