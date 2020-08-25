#!/usr/bin/env python
import socket
import select
import sys
import shlex
import struct
import fcntl
import os
import time
import logging
import subprocess
logging.basicConfig(filename='/var/log/labdump_client.log', level=logging.DEBUG)
eth_name = sys.argv[1]
netname = sys.argv[2]
mac = sys.argv[3]
server = sys.argv[4]
port = int(sys.argv[5])
logging.info('labdump client for netname %s server %s port %d eth %s mac: %s' % (netname, 
    server, port, eth_name, mac))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (server, port)
while True:
    try:
        sock.connect(server_addr)
        break
    except:
        logging.debug('labdump client connect failed, sleep 3')
        time.sleep(3)

logging.debug('labdump client connect success')

cmd = '/usr/bin/tcpdump -U -w - -i %s "not (ether host %s and (port 5353 or icmp or icmp6))"' % (eth_name, mac)
logging.debug('cmd is %s' % cmd)
ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
logging.debug('ran popen')
''' non blocking for ps.stdout '''
try:
    orig_fl = fcntl.fcntl(ps.stdout, fcntl.F_GETFL)
    fcntl.fcntl(ps.stdout, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)
except:
    e = sys.exc_info()[0]
    logging.error('fcntl error %s\n' % e)
    exit(1)

logging.debug('did fcntl ')
netname_len = len(netname)
v = struct.pack('I', netname_len)
''' length/value for lan name '''
both = v+netname
sock.sendall(both)
logging.debug('labdump client sent netname')
try:
    while True:
        if ps.stdout in select.select([ps.stdout], [], [], 3)[0]:
            try:
                data = ps.stdout.read()
            except:
                e = sys.exc_info()[0]
                logging.error('read error %s\n' % e)
                #exit(1)
            try:
                sock.sendall(data)
            except:
                e = sys.exc_info()[0]
                logging.error('send error %s\n' % e)
                exit(1)
        else:
            #logging.debug('labdump client, no data')
            pass
except:
    e = sys.exc_info()[0]
    logging.error('select error %s\n' % e)
    exit(1)

