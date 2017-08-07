#!/usr/bin/env python
import socket
import sys
import os
import signal
import subprocess

'''
Manage loading of PLC firmware.  Listen to a TCP socket for a
connection.  The protocol is a four byte length field (represented
as an ascii string) followed by the data.  On each connection,
the first data goes to the code file, the second to the config.txt
file. After firmware is loaded, the PLC executes.
'''

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('172.26.0.3', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

def sendData(connection, data):
    size = len(data)
    size_str = '%4d' % size
    connection.sendall(size_str)
    connection.sendall(data)


def getData(connection):
    rbytes = ''
    try:
        #print('getData get size')
        size_str = connection.recv(4)
        if size_str is None or len(size_str) == 0:
            return None
        try:
            size = int(size_str)
        except:
             print >>sys.stderr, 'getData could not parse int from <%s>' % size_str
             exit(1)
        #print('expect %d bytes' % size)
        # Receive the data, but only up to size bytes 
        remaining = size
        while len(rbytes) < size:
            data = connection.recv(remaining)
            remaining = remaining - len(data)
            print >>sys.stderr, 'received "%d bytes"' % len(data)
            if data:
                rbytes = rbytes + data
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
        print >>sys.stderr, 'done read, got total of %d bytes' % len(rbytes)
    except socket.error:
        print >>sys.stderr, 'proxy socket error %s' % str(socket.error)
        connection.close()
        rbytes = None
    return rbytes


def signal_handler(signal, frame):
    global connection
    connection.close()
    print >>sys.stderr, 'got signal, bye'
    exit(0)

connection = None
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
ps = None
status = False
while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    connection.setblocking(True)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print >>sys.stderr, 'connection from', client_address
    
    rbytes = getData(connection)
    if rbytes is None:
        break
    parts = rbytes.split(':',1)
    if parts[0] == 'load':
        if ps is not None:
            ps.send_signal(signal.SIGINT)
            print >>sys.stderr, 'signal sent to PLC, wait for it to die'
            ps.wait()
            print >>sys.stderr, 'PLC has terminated, load new firmware'
        data = parts[1]
        with open('plc', 'w') as fh:
            os.chmod('plc', 0o777)
            fh.write(data)
            fh.close
            print >>sys.stderr, 'code file closed'
        data = getData(connection)
        with open('config.txt', 'w') as fh:
            os.chmod('config.txt', 0o777)
            fh.write(data)
            fh.close
            print >>sys.stderr, 'config file closed'
        ps  = subprocess.Popen('./plc', shell=False)
        status = True
    elif parts[0] == 'status':
        #print('is status, send reply')
        sendData(connection, 'status:%s' % status)    
    elif parts[0] == 'retrieve':
        with open('plc', 'r') as fh:
            sendData(connection, fh.read())
        with open('config.txt', 'r') as fh:
            sendData(connection, fh.read())


    print >>sys.stderr, 'closing connection'
    connection.close()
    
