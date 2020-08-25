#!/usr/bin/env python
import socket
import threading
import struct
import os
import logging
def getFname(net_name):
    fname = os.path.join('/taps', net_name+'.pcap')
    i = 1
    while os.path.isfile(fname): 
        fname = os.path.join('/taps', (net_name+'.%d.pcap' % i))
        i += 1
    return fname
def handleClient(conn, logging):
    nlen = conn.recv(4)
    ''' look for test connections and bail '''
    if nlen is None or len(nlen) == 0:
        logging.debug('client got zilch')
        return
    try:
        nlen_val = struct.unpack('I', nlen)[0]
    except:
        logging.debug('client got garbage')
        return
    net_name = conn.recv(nlen_val)
    logging.info('net name is %s\n' % net_name)
    try:
        os.mkdir('/taps')
    except:
        pass
    fname = getFname(net_name)
    outfile = open(fname, 'a')
    while True:
        data = conn.recv(1024)
        if len(data) == 0:
            break
        #logging.debug('got %d bytes' % len(data))
        outfile.write(data)
        outfile.flush()


logging.basicConfig(filename='/var/log/labdump_server.log', level=logging.DEBUG)
server = ('0.0.0.0', 1929)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server)
sock.listen(1)
while True:
    conn, addr = sock.accept()
    logging.info('connect from %s' % str(addr))
    x = threading.Thread(target=handleClient, args=(conn, logging))
    x.start()
sock.close()

