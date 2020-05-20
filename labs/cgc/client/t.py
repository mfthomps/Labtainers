#!/usr/bin/env python
import socket
HOST = '172.25.0.3'  # The server's hostname or IP address
PORT = 60606        # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('back from connect')
data = s.recv(1000)
print(data)

