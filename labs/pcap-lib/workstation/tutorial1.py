import dpkt 
import socket
import sys

fd = open('trace2.pcap', 'rb')
pcap = dpkt.pcap.Reader(fd)

for ts, data in pcap:
  print ts
  for char in data:
    print hex(ord(char)),
  print
  e = dpkt.ethernet.Ethernet(data) 
  ip = e.data
  print "\nIP version:", ip.v
  print "IP source:", socket.inet_ntoa(ip.src)
  sys.exit(-1)