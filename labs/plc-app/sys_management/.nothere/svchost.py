#!/usr/bin/env python
import socket
import sys
import subprocess
import time
import logging


def doConnect():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('172.25.0.3', 10000)
    #print >>sys.stderr, 'connecting to %s port %s' % server_address
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


LOGFILE = "/tmp/mgmt.log"
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)
logging.debug("hi from svchost")


while True:
    p = subprocess.Popen(['tcpdump', '-l', '-XX', '-i', 'eth0',  '--direction=out'],  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    logging.debug("tcpdump running")
    for row in iter(p.stdout.readline, b''):
        #print row.rstrip() 
        #if 'plc.proxy.student.management_lan' in row:
        if 'load:' in row:
            #print(' got it ')
            time.sleep(2)
            sock = doConnect()
            doSend(sock, 'status:')
            data = getData(sock)
            sock.close()
            logging.debug("found load in tcpdump, data is: %s" % data)
            if "Params: 20 30" in data:
                logging.debug('Is dry config, send the program')
                break
    
    #print 'out of loop'
    time.sleep(25)
    
    logging.debug("connect and send code")
    sock = doConnect()
    plc_code = './plc'
    plc_config = './config.txt'
    #print('plc_code is %s data is %s' % (plc_code, plc_config))
    with open(plc_code, mode='rb') as fh:
        code = fh.read();
        doSend(sock, 'load:'+code)
    with open(plc_config, mode='rb') as fh:
        config = fh.read();
        doSend(sock, config)
    sock.close()
    logging.debug("done, bye")
    p.kill()
    p.wait()
