#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
import os
import sys

PORT = 80

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

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT

httpd.serve_forever()
