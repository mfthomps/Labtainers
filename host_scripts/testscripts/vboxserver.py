#!/usr/bin/env python3
import socket
import sys
import subprocess
'''

'''

def doCommand(cmd):
    vb_cmd = 'vboxmanage %s' % cmd
    ps = subprocess.Popen(vb_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ps.communicate()
    retval = ''
    for line in output[0].decode('utf-8').splitlines():
        print(line)
        retval += line+'\n'
    for line in output[1].decode('utf-8').splitlines():
        print(line)
        retval += line+'\n'
    return retval

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = ('192.168.1.223', 6000)
    print('do bind')
    sock.bind(server_addr)
    while True:
        got, addr = sock.recvfrom(4096)
        #print('g %s addr %s' % (got, addr))
        if got is None or len(got) == 0:
            print('got zilch, quit')
            exit(0)
        got = got.decode()
        print('got %s' % got) 
        result = doCommand(got)
        sock.sendto(result.encode(), addr)
