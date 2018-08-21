#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
import base64
import os
import sys

PORT = 80
AUTHFILELIST = "/sbin/authfile.list"
AUTHLIST = "/sbin/auth.list"

class MyHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    key = []
    authfilenameslist = []
    #log_file = open('myhttplogfile.txt', 'w')
    log_file = open('/var/log/myhttplogfile.txt', 'w')

    def check_filepath(self, inputpath):
        auth_needed = False
        #print self.authfilenameslist
        for fname in self.authfilenameslist:
            #print "The requested path is (%s) and fname is (%s)" % (self.path, fname)
            if fname in inputpath:
                auth_needed = True
                break
        return auth_needed

    def check_authorize(self, authorization):
        authorized = False
        #print "Current authorization is (%s)" % authorization
        for authkey in self.key:
            authorized_key = 'Basic ' + authkey
            #print "authorized_key is (%s)" % authorized_key
            if authorized_key == authorization:
                #print "matched"
                authorized = True
                break
        return authorized

    def log_message(self, format, *args):
        self.log_file.write("%s - - [%s] %s\n" %
                            (self.client_address[0],
                             self.log_date_time_string(),
                             format%args))
        self.log_file.flush()

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Secure HTTP Environment\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #if self.path != None:
        #    print "The requested path is (%s)" % self.path

        if self.check_filepath(self.path):
            if self.headers.getheader('Authorization') is None:
                self.do_AUTHHEAD()
                self.wfile.write('No auth received')
            elif self.check_authorize(self.headers.getheader('Authorization')):
                SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.do_AUTHHEAD()
                self.wfile.write(self.headers.getheader('Authorization'))
                self.wfile.write('Not authenticated')
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyHTTPHandler
authfilelist = open(AUTHFILELIST)
Handler.authfilenameslist = authfilelist.read().splitlines()
#print Handler.authfilenameslist
authlist = open(AUTHLIST)
authnamepass = authlist.read().splitlines()
for namepass in authnamepass:
    curkey = base64.b64encode(namepass.strip())
    Handler.key.append(curkey)

httpd = SocketServer.TCPServer(("", PORT), Handler)

#print "serving at port", PORT

httpd.serve_forever()

