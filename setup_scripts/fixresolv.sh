#!/bin/bash

sudo rm -f /tmp/fixresolv.tmp
echo "search ern.nps.edu" > /tmp/fixresolv.tmp
echo "nameserver 172.20.20.12" >> /tmp/fixresolv.tmp
echo "nameserver 172.20.20.11" >> /tmp/fixresolv.tmp
sudo cp /tmp/fixresolv.tmp /run/resolvconf/interface/NetworkManager
sudo resolvconf -u

# Verify /etc/resolv.conf
cat /etc/resolv.conf
