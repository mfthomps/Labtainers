#!/usr/bin/env python3
import socket
import sys
import subprocess
'''

'''

def doCommand(cmd, log):
    vb_cmd = 'vboxmanage %s' % cmd
    ps = subprocess.Popen(vb_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ps.communicate()
    retval = ''
    for line in output[0].decode('utf-8').splitlines():
        log.write(line+'\n')
        retval += line+'\n'
    for line in output[1].decode('utf-8').splitlines():
        log.write(line+'\n')
        retval += line+'\n'
    return retval

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #server_addr = ('192.168.122.1', 6000)
    server_addr = ('10.20.200.41', 6000)
    logfile='/tmp/vboxserver.log'
    log = open(logfile,'w')
    log.write('do bind'+'\n')
    sock.bind(server_addr)
    while True:
        got, addr = sock.recvfrom(4096)
        #print('g %s addr %s' % (got, addr))
        if got is None or len(got) == 0:
            log.write('got zilch, quit'+'\n')
            exit(0)
        got = got.decode()
        log.write('got %s\n' % got) 
        result = doCommand(got, log)
        sock.sendto(result.encode(), addr)
