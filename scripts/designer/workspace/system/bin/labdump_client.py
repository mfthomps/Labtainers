#!/usr/bin/env python
import socket
import select
import sys
import struct
import fcntl
import os
import time
netname = sys.argv[1]
server = sys.argv[2]
port = int(sys.argv[3])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (server, port)
while True:
    try:
        sock.connect(server_addr)
        break
    except:
        time.sleep(3)

netname_len = len(netname)
v = struct.pack('I', netname_len)
''' length/value for lan name '''
both = v+netname
sock.sendall(both)
''' set non blocking '''
orig_fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
fcntl.fcntl(sys.stdin, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)

while True:
    if select.select([sys.stdin], [], [], 3):
        data = sys.stdin.read()
        sock.sendall(data)
    else:
        print('no data')
        pass

