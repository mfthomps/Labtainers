#!/usr/bin/env python
import socket
import sys
import time
import signal
import threading
import hashlib
import logging

def signal_handler(signal, frame):
    global connection
    global response_thread
    logging.debug('got signal, close connection')
    if connection is not None:
        connection.close()
    logging.debug('no exit')
    exit(0)


def getData(connection, who):
    '''
    Read data from the connection based on its initial 4 character size field.
    The who field is simply for debugging.
    '''
    rbytes = ''
    try:
        #logging.debug('%s getData get size' % who)
        size_str = connection.recv(4)
        if size_str is None or len(size_str) == 0:
            logging.debug('%s client closed' % who)
            return None
        try:
            size = int(size_str)
        except:
             logging.debug('getData could not parse int from <%s>' % size_str)
             exit(1)
        #logging.debug('%s getData size is %d' % (who, size))
        # Receive the data, but only up to size bytes 
        remaining = size
        while len(rbytes) < size:
            data = connection.recv(remaining)
            remaining = remaining - len(data)
            #logging.debug('received "%d bytes"' % len(data))
            if data:
                rbytes = rbytes + data
            else:
                logging.debug('no more data from', client_address)
                break
        logging.debug('%s done read, got total of %d bytes' % (who, len(rbytes)))
    except socket.error:
        logging.debug('proxy socket error %s' % str(socket.error))
        connection.close()
        rbytes = None
    return rbytes

def sendData(connection, data, who):
    '''
    Send data to the connection, prefixed by a four character length field.
    The who field is simply for debugging
    '''
    size = len(data)
    logging.debug('%s sendData %d bytes' % (who, size))
    size_str = '%4d' % size
    connection.sendall(size_str)
    connection.sendall(data)

def responses(connection, remote_sock):
    #logging.debug('in responses')
    rdata = ''
    while rdata is not None:
        rdata = getData(remote_sock, 'from-plc')
        #logging.debug('responses back from getData with %s' % rdata)
        if rdata is not None:
            sendData(connection, rdata, 'responses')
        else:
            logging.debug('responses got None from-plc')
    exit()
 
def checkData(data):
    retval = True
    if data is None:
        retval = False
    elif data != 'status:' and data != 'retrieve:' and data != 'reset:':
         if data.startswith('load'):
             data = data[5:]
         if 'bad stuff' in data:
             retval = False
    return retval

def main():
    global connection
    global response_thread
    sys.stderr = open('err.txt', 'w')
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Create a TCP/IP socket for proxy server & client
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_server_address = ('172.25.0.3', 10000)
    remote_server_address = ('172.26.0.3', 10000)
    logging.debug('starting up on %s port %s' % local_server_address)
    sock.bind(local_server_address)
    # Listen for incoming connections
    sock.listen(1)
    while True:
        # Wait for a connection
        logging.debug('waiting for a connection')
        connection, client_address = sock.accept()
        connection.setblocking(True)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_sock.connect(remote_server_address)
        remote_sock.setblocking(True)
        remote_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        response_thread = threading.Thread(target=responses, args=(connection, remote_sock))
        response_thread.start()
        rdata = ''
    
        while rdata is not None:
            rdata = getData(connection, 'from-manager')
            if checkData(rdata):
                sendData(remote_sock, rdata, 'to-server')
            elif rdata is not None:
                logging.debug('Data failed check, dropping it!')
            else:
                logging.debug('got None from getData from-manager')
        logging.debug('close the connections, we got None') 
        time.sleep(1)
        connection.close()
        try:
            remote_sock.shutdown(socket.SHUT_RDWR)
            remote_sock.close()
        except socket.error, msg:
            logging.debug('Failed to close remote_sock, client dropped?: %s' % msg)
        

LOGFILE = "./proxy.log"
print("logging to ./proxy.log")
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)
logging.debug("Starting proxy")
logging.debug("The proxy is started with: sudo /etc/init.d/proxy.sh start|stop")
global connection
connection = None        
main()
