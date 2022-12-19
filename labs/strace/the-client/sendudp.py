#!/usr/bin/env python
import sys
import socket
host = '10.10.0.2'
if len(sys.argv) < 2:
    print('./sendudp.py <port>')
    exit(1)
try:
    port = int(sys.argv[1])
except:
    print('bad port number')
    exit(1)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (host, port)
msg = str.encode("HI THERE")
sock.sendto(msg, server_addr)
sock.settimeout(5)
try:
    got = sock.recvfrom(1024)
    print(got[0].decode('utf-8'))
except:
    print("No reply from %d" % port)
