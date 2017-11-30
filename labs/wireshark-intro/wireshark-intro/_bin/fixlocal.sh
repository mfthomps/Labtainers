#!/bin/bash

# DUMMY

cd $HOME
# Do editcap to new file to avoid potential corruption
editcap -t EDITCAP_SECONDS telnet.pcap new.telnet.pcap
# Replace when done
cp telnet.pcap /tmp/
mv new.telnet.pcap telnet.pcap

