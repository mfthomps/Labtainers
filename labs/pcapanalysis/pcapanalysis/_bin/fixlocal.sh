#!/bin/bash

cd $HOME
# Do editcap to new file to avoid potential corruption
editcap -t EDITCAP_SECONDS tcpdump.telnet.pcap new.tcpdump.telnet.pcap
# Replace when done
mv new.tcpdump.telnet.pcap tcpdump.telnet.pcap

