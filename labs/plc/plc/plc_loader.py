#!/usr/bin/env python
import socket
import sys
import time
import os
import signal
import subprocess
import ctypes
import mmap
import logging

'''
Manage loading of PLC firmware.  Listen to a TCP socket for a
connection.  The protocol is a four byte length field (represented
as an ascii string) followed by the data.  On each connection,
the first data goes to the code file, the second to the config.txt
file. After firmware is loaded, the PLC executes.
'''

# Create a TCP/IP socket
LOGFILE = "./plc_loader.log"
print("logging to %s" % LOGFILE)
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)
logging.debug("Starting plc_loader")
filename='/tmp/iodevice'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('172.26.0.3', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

def doMap(): 
    # Create new empty file to back memory map on disk
    # and return the buf associated with it
    logging.debug('doMap try open %s' % filename)
    fd = os.open(filename, os.O_CREAT | os.O_TRUNC | os.O_RDWR)

    # Zero out the file to insure it's the right size
    assert os.write(fd, '\x00' * mmap.PAGESIZE) == mmap.PAGESIZE

    # Create the mmap instace with the following params:
    # fd: File descriptor which backs the mapping or -1 for anonymous mapping
    # length: Must in multiples of PAGESIZE (usually 4 KB)
    # flags: MAP_SHARED means other processes can share this mmap
    # prot: PROT_WRITE means this process can write to this mmap
    buf = mmap.mmap(fd, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE)
    return buf

def sendData(connection, data):
    size = len(data)
    size_str = '%4d' % size
    try:
        connection.sendall(size_str)
        connection.sendall(data)
    except socket.error, msg:
        logging.debug('Failed sending data, socket error, could be client dropped: %s' % msg)


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
             logging.debug('getData could not parse int from %s' % size_str)
             print >>sys.stderr, 'getData could not parse int from <%s>' % size_str
             exit(1)
        logging.debug('expect %d bytes' % size)
        # Receive the data, but only up to size bytes 
        remaining = size
        while len(rbytes) < size:
            data = connection.recv(remaining)
            remaining = remaining - len(data)
            print >>sys.stderr, 'received "%d bytes"' % len(data)
            logging.debug('received "%d bytes"' % len(data))
            if data:
                rbytes = rbytes + data
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
        print >>sys.stderr, 'done read, got total of %d bytes' % len(rbytes)
        logging.debug('done read, got total of %d bytes' % len(rbytes))
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
buf = doMap()
logging.debug('back from doMap')
pump_running = ctypes.c_int.from_buffer(buf, 4)
loader_ready = ctypes.c_int.from_buffer(buf, 8)
reset_counter = ctypes.c_int.from_buffer(buf, 12)
reset_counter.value = 1
loader_ready.value = 1
logging.debug('set ready to 1')
while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    logging.debug('waiting for a connection')
    connection, client_address = sock.accept()
    connection.setblocking(True)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print >>sys.stderr, 'connection from', client_address
    logging.debug('connection from %s:%s' % (client_address[0], client_address[1]))
    
    rbytes = getData(connection)
    if rbytes is None:
        logging.debug('Read None from getData, dropped by proxy?')
    else:
        parts = rbytes.split(':',1)
        load_ok = True
        if parts[0] == 'load':
            logging.debug('load command')
            if ps is not None:
                ps.send_signal(signal.SIGINT)
                print >>sys.stderr, 'signal sent to PLC, wait for it to die'
                logging.debug('signal sent to PLC, wait for it to die')
                time.sleep(2)
                if ps.poll() is None:
                    load_ok = False
                    logging.debug('PLC still running, ignored signal?')
                else:
                    print >>sys.stderr, 'PLC has terminated, load new program'
                    logging.debug('PLC terminated, load new program')
            if load_ok:
                data = parts[1]
                with open('plc', 'w') as fh:
                    os.chmod('plc', 0o777)
                    fh.write(data)
                    fh.close
                    print >>sys.stderr, 'code file closed'
                data = getData(connection)
                if rbytes is None:
                    logging.debug('Read None from getData, dropped by proxy?')
                else:
                    with open('config.txt', 'w') as fh:
                        os.chmod('config.txt', 0o777)
                        fh.write(data)
                        fh.close
                        print >>sys.stderr, 'config file closed'
                    ps  = subprocess.Popen('./plc', shell=False)
                    status = True
                sendData(connection, 'Program and configuration loaded into PLC')
            else:
                sendData(connection, 'Error: Existing PLC program failed to terminate!')
        elif parts[0] == 'status':
            #print('is status, send reply')
            logging.debug('status command')
            sendData(connection, 'status:%s' % status)    
        elif parts[0] == 'retrieve':
            logging.debug('retrieve command')
            if os.path.isfile('plc'):
                with open('plc', 'r') as fh:
                    sendData(connection, fh.read())
                with open('config.txt', 'r') as fh:
                    sendData(connection, fh.read())
            else:
                sendData(connection, 'no file')
                sendData(connection, 'no file')
        elif parts[0] == 'reset':
            logging.debug('reset command')
            if ps is not None:
                ps.kill()
                print >>sys.stderr, 'PLC killed'
                logging.debug('back from kill')
                pump_running.value = 0
                status = False
                ps = None
                reset_counter.value += 1


    print >>sys.stderr, 'closing connection'
    logging.debug('closing connection')
    connection.close()
    
