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
import socket

def get_hw_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if sys.version_info >=(3,0):
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
        return ':'.join('%02x' % b for b in info[18:24])
    else:
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', str(ifname[:15])))
        return ':'.join(['%02x' % ord(char) for char in info[18:24]])


'''
Start tcpdump a tapped interface, but ignore icmp, 5353 and traffic from the mac of the interface,
intended to be the mac of the bridge on the host. 
'''
logging.basicConfig(filename='/var/log/labdump_client.log', level=logging.DEBUG)
eth_name = sys.argv[1]
netname = sys.argv[2]
mac = get_hw_address(eth_name)
server = sys.argv[3]
port = int(sys.argv[4])
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

