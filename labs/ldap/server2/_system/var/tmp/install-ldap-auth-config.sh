#!/bin/bash
#
# Hacked script to automate installation of ldap-auth-config.sh
# The usual debconf-set-selections fails on ldap-auth-config becuase
# it prompts first for a mother-may-I.  
# This script is intended to be named in the VISUAL environment variable
# when the dpkg-reconfig is run with the editor front end:
#      dpkg-reconfigure -feditor ldap-auth-config
#
#
fid=$1
override=$(grep override $1)
if [[ ! -z "$override" ]]; then
    echo "IS OVERRIDE"
    cp /var/tmp/dogs/dog1.txt $1
else
    server=$(grep "LDAP server Uniform Resource" $1)
    if [[ ! -z "$server" ]]; then
        echo "IS SERVER"
        cp /var/tmp/dogs/dog2.txt $1
    else
        local_root=$(grep "Make local root Database" $1)
        if [[ ! -z "$local_root" ]]; then
            echo "IS LOCAL ROOT"
            cp /var/tmp/dogs/dog3.txt $1
        else
            root_account=$(grep "LDAP account for root" $1)
            if [[ ! -z "$root_account" ]]; then
                echo "IS ROOT ACCOUNT"
                cp /var/tmp/dogs/dog4.txt $1
            else
                pam_fu=$(grep "The PAM module can set the" $1)
                if [[ ! -z "$pam_fu" ]]; then
                    echo "IS pam fu"
                    cp /var/tmp/dogs/dog5.txt $1

                fi
            fi
        fi
    fi
fi
