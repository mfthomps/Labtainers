#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
import os
import sys
import random

PORT0 = random.randint(5000, 9999)
PORT1 = random.randint(5000, 9999)
PORT2 = random.randint(5000, 9999)
PORT3 = random.randint(5000, 9999)
PORT4 = random.randint(5000, 9999)

class MyHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    #log_file = open('myhttplogfile.txt', 'w')
    log_file = open('/var/log/myhttplogfile.txt', 'w')
    def log_message(self, format, *args):
        self.log_file.write("%s - - [%s] %s\n" %
                            (self.client_address[0],
                             self.log_date_time_string(),
                             format%args))
        self.log_file.flush()

Handler = MyHTTPHandler

httpd0 = SocketServer.TCPServer(("", PORT0), Handler)
httpd1 = SocketServer.TCPServer(("", PORT1), Handler)
httpd2 = SocketServer.TCPServer(("", PORT2), Handler)
httpd3 = SocketServer.TCPServer(("", PORT3), Handler)
httpd4 = SocketServer.TCPServer(("", PORT4), Handler)

httpd0.serve_forever()
httpd1.serve_forever()
httpd2.serve_forever()
httpd3.serve_forever()
httpd4.serve_forever()
