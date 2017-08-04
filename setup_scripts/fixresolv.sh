#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
END
: <<'END'
Add the hosts DNS servers to the /etc/resolv.conf by appending them
to the resolv.conf.d/head file.  Some dockers, ubuntu?, cannot resolve
addresses from within containers.
END
dns_list=$(nmcli dev show | grep DNS | awk '{print $2 $4}')
echo already is $dns_list
for dns in $dns_list
do
    already=$(grep $dns /etc/resolvconf/resolv.conf.d/head)
    if [ -z "$already" ]; then
        echo "nameserver $dns" | sudo tee -a /etc/resolvconf/resolv.conf.d/head
    fi
done
sudo resolvconf -u

# Verify /etc/resolv.conf
echo "resolveconf now contains:"
cat /etc/resolv.conf
