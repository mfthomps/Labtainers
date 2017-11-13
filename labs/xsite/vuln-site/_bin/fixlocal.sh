#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
while [ 1 ]; do
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

