#!/usr/bin/env python3
import socket
import sys
import argparse
all_args = ' '.join(sys.argv[1:])
PORT = 60000
host = '127.0.0.1'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Display and alter state of a Labtainer exercise on remote VM.')
    parser.add_argument('-l', '--lab', action='store', help='manage this lab')
    parser.add_argument('-c', '--copy', action='store', help='Copy files per the named directive.')
    parser.add_argument('-s', '--status', action='store_true', default=False, help='status of lab on this VM')
    parser.add_argument('-p', '--port', action='store', default=PORT, help='Remote port, default is %d' % PORT)
    parser.add_argument('-d', '--destination', action='store', default=host, help='Remote host, default is %s' % host)
    args = parser.parse_args()

    server = (args.destination, args.port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server)
    if args.status:
        sock.sendall(b'status')
        got = sock.recv(1024)
        print(got.decode('utf-8'))
    elif args.copy is not None:
        if args.lab is not None:
            cmd = 'copy %s %s' % (args.lab, args.copy)
            sock.sendall(cmd.encode())
            got = sock.recv(1024)
            print(got.decode('utf-8'))
        else:
            print('Need --lab argument')
            args.usage()
    else:
        print('Need --copy argument')
        args.usage()
    sock.close()
