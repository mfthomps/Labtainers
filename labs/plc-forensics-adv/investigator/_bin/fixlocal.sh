#!/bin/bash

cd $HOME
# Do editcap to new file to avoid potential corruption
editcap -t EDITCAP_SECONDS Task1-trace.pcap new.Task1-trace.pcap
editcap -t EDITCAP_SECONDS Task2-trace.pcap new.Task2-trace.pcap
editcap -t EDITCAP_SECONDS Task3-trace.pcap new.Task3-trace.pcap
editcap -t EDITCAP_SECONDS Task4-trace1.pcap new.Task4-trace1.pcap
editcap -t EDITCAP_SECONDS Task4-trace2.pcap new.Task4-trace2.pcap
editcap -t EDITCAP_SECONDS Task5-trace.pcap new.Task5-trace.pcap
# Replace when done
mv new.Task1-trace.pcap Task1-trace.pcap
mv new.Task2-trace.pcap Task2-trace.pcap
mv new.Task3-trace.pcap Task3-trace.pcap 
mv new.Task4-trace1.pcap Task4-trace1.pcap 
mv new.Task4-trace2.pcap Task4-trace2.pcap 
mv new.Task5-trace.pcap Task5-trace.pcap 

