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


LOGFILE = "/tmp/mgmt.log"
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)
logging.debug("hi from svchost")


#p = subprocess.Popen(['tcpdump', '-l', '-i', 'eth0', '--direction=in', "(tcp[tcpflags] & (tcp-fin|tcp-rst)) != 0"],  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p = subprocess.Popen(['tcpdump', '-l', '-XX', '-i', 'eth0',  '--direction=out'],  stdout=subprocess.PIPE, stderr=subprocess.PIPE)

logging.debug("tcpdump running")
for row in iter(p.stdout.readline, b''):
    #print row.rstrip() 
    #if 'plc.proxy.student.management_lan' in row:
    if 'load:' in row:
        #print(' got it ')
        logging.debug("found load in tcpdump")
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
