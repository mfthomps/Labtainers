#!/usr/bin/env python3
import sys
import socket
import argparse
'''
Manage VBox clients on a remote system -- indended to be system that hosts the VM
upon which this script is invoked. 
'''
'''
'''
hstring = 'list runningvms\nlist vms\ncontrolvm <vm>reset\ncontrolvm <vm> poweroff\nstartvm <vm>'
server_addr = ('10.20.200.41', 6000)
parser = argparse.ArgumentParser(prog='vbox-client.py', formatter_class=argparse.RawTextHelpFormatter, description='Start a VBox vm on %s\n%s' % (server_addr[0], hstring))
parser.add_argument('command', action='store', help='The command to run, in quotes')

args = parser.parse_args()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cmd = ' '.join(sys.argv[1:])
print('cmd is %s' % cmd)
sent = sock.sendto(cmd.encode(), server_addr)
reply, addr = sock.recvfrom(4096)
print(reply.decode())
print('done')
