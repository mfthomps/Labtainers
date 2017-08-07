#!/usr/bin/env python
import socket
import sys

def usage():
    print('manage_client [code] [config]')
    exit(0)

def doConnect():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('172.25.0.3', 10000)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    return sock

def doSend(sock, data):
    size = len(data)
    size_str = '%4d' % size
    sock.sendall(size_str)
    sock.sendall(data)

if len(sys.argv) != 3:
    usage()
sock = doConnect()
plc_code = sys.argv[1]
plc_config = sys.argv[2]
print('plc_code is %s data is %s' % (plc_code, plc_config))
with open(plc_code, mode='rb') as fh:
    code = fh.read();
    doSend(sock, code)
with open(plc_config, mode='rb') as fh:
    config = fh.read();
    doSend(sock, config)
sock.close()
