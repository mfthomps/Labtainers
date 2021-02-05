#!/bin/bash

# DUMMY

cd $HOME
# Do editcap to new file to avoid potential corruption
editcap -F pcap -r telnet.pcap new.telnet.pcap EDITCAP_START-999999
mv new.telnet.pcap telnet.pcap
