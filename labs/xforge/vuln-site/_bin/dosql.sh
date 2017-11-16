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
