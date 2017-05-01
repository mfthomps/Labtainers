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
sudo rm -f /tmp/fixresolv.tmp
echo "search ern.nps.edu" > /tmp/fixresolv.tmp
echo "nameserver 172.20.20.12" >> /tmp/fixresolv.tmp
echo "nameserver 172.20.20.11" >> /tmp/fixresolv.tmp
sudo cp /tmp/fixresolv.tmp /run/resolvconf/interface/NetworkManager
sudo resolvconf -u

# Verify /etc/resolv.conf
cat /etc/resolv.conf
