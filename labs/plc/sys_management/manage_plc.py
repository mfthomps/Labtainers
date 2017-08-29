#!/usr/bin/env python
import socket
import sys
import argparse


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

def getData(connection):
    rbytes = ''
    try:
        size_str = connection.recv(4)
        if size_str is None or len(size_str) == 0:
            return None
        try:
            size = int(size_str)
        except:
             print >>sys.stderr, 'getData could not parse int from <%s>' % size_str
             exit(1)
        # Receive the data, but only up to size bytes 
        remaining = size
        while len(rbytes) < size:
            data = connection.recv(remaining)
            remaining = remaining - len(data)
            #print >>sys.stderr, 'received "%d bytes"' % len(data)
            if data:
                rbytes = rbytes + data
            else:
                #print >>sys.stderr, 'no more data from', client_address
                break
        #print >>sys.stderr, 'done read, got total of %d bytes' % len(rbytes)
    except socket.error:
        print >>sys.stderr, 'proxy socket error %s' % str(socket.error)
        connection.close()
        rbytes = None
    return rbytes

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')
load_parser = subparsers.add_parser('load', help='load program and configuration data into the PLC')
load_parser.add_argument('program', type=str, help='File name of the program')
load_parser.add_argument('configuration', type=str, help='File name of the configuration data')
status_parser = subparsers.add_parser('status', help='determine if the plc is running')
status_parser = subparsers.add_parser('retrieve', help='Get program and data from the plc and store in local file')


args = parser.parse_args()

sock = doConnect()
sock.setblocking(True)
if args.command == 'status':
    doSend(sock, 'status:')
    #print('command sent')
    data = getData(sock)
    #print('reply received')
    if data == 'status:True':
        print('PLC is running')
    else:
        print('PLC is not running')

elif args.command == 'load':
    print('plc_code is %s data is %s' % (args.program, args.configuration))
    with open(args.program, mode='rb') as fh:
        code = fh.read();
        doSend(sock, 'load:'+code)
    with open(args.configuration, mode='rb') as fh:
        config = fh.read();
        doSend(sock, config)
elif args.command == 'retrieve':
    code_file = 'plc_code.retrieved'
    config_file = 'plc_config.retrieved'
    doSend(sock, 'retrieve:')
    code = getData(sock)
    config = getData(sock)
    with open(code_file, 'w') as fh:
        fh.write(code)
    with open(config_file, 'w') as fh:
        fh.write(config)
    print('Retreived PLC code/data into %s and %s' % (code_file, config_file))

sock.close()
