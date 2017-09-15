#!/bin/bash

cd $HOME
# Do editcap to new file to avoid potential corruption
editcap -t EDITCAP_SECONDS telnet.pcap new.telnet.pcap 1-START_FRAME
# Replace when done
cp telnet.pcap /tmp/
mv new.telnet.pcap telnet.pcap

