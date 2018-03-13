import os
import sys

os.system('tcprewrite --pnat=10.0.0.0:192.168.1.0,172.16.0.0:192.168.1.0 --infile=Teredo.pcap --outfile=Teredo.pcap')
os.system('tcpreplay --loop=0 --intf1=eth0 /root/Desktop/attacks/Teredo.pcap')
