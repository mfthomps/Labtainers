#!/usr/bin/env python3
'''
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''

import inspect
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import re
import ParseLabtainerConfig

LABTAINER_CONFIG = os.path.abspath("../../config/labtainer.config")

'''
NOTE: will redefine logfilename to be relative to LABTAINER_DIR/logs if that
env variable exists.
'''

class LabtainerLogging():
    def __init__(self, logfilename, labname, labtainer_config):
        #print "filename is (%s)" % logfilename
        #print "labname is (%s)" % labname
        logname = "labtainer.%s" % labname

        labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config, None)
        file_log_level = labtainer_config.file_log_level
        console_log_level = labtainer_config.console_log_level

        self.logger = logging.getLogger(logname)
        self.logger.setLevel(file_log_level)
        formatter = logging.Formatter('[%(asctime)s - %(levelname)s : %(message)s')
        ldir = os.getenv('LABTAINER_DIR')
        if ldir is not None:
            if not os.path.isdir(ldir):
                print('Warning, LABTAINER_DIR value %s is not a directory' % ldir)
                ldir =  os.path.join(os.getenv('HOME'), 'labtainer', 'trunk')
                if not os.path.isdir(ldir):
                    print('Unable to find LABAINER_DIR, be sure env variable is set.')
                    exit(1)
        else:
            ldir =  os.path.join(os.getenv('HOME'), 'labtainer', 'trunk')
            if not os.path.isdir(ldir):
                print('Unable to find LABAINER_DIR, be sure env variable is set.')
                exit(1)
        if ldir is not None and not logfilename.startswith(ldir):
           if logfilename.startswith('/tmp/'):
               logfilename = logfilename[5:]
           logfilename = os.path.join(ldir,'logs',logfilename)
           try:
               os.makedirs(os.path.dirname(logfilename))
           except:
               pass
        #file_handler = logging.FileHandler(logfilename)
        file_handler = RotatingFileHandler(logfilename, maxBytes=6000000, backupCount=3)
        file_handler.setLevel(file_log_level)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_log_level)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.file_name = logfilename

    def debug(self, message):
        func = inspect.currentframe().f_back
        #print "func.f_code.co_name is %s" % func.f_code.co_name
        #print "func.f_code.co_filename is %s" % func.f_code.co_filename
        #print "func.f_lineno is %s" % func.f_lineno
        filename = os.path.basename(func.f_code.co_filename)
        lineno = func.f_lineno
        funcname = func.f_code.co_name
        linemessage = '%s:%s - %s() ] %s' % (filename, lineno, funcname[:15], message)
        self.logger.debug(linemessage)

    def info(self, message):
        func = inspect.currentframe().f_back
        #print "func.f_code.co_name is %s" % func.f_code.co_name
        #print "func.f_code.co_filename is %s" % func.f_code.co_filename
        #print "func.f_lineno is %s" % func.f_lineno
        filename = os.path.basename(func.f_code.co_filename)
        lineno = func.f_lineno
        funcname = func.f_code.co_name
        linemessage = '%s:%s - %s() ] %s' % (filename, lineno, funcname[:15], message)
        self.logger.info(linemessage)

    def warning(self, message):
        func = inspect.currentframe().f_back
        #print "func.f_code.co_name is %s" % func.f_code.co_name
        #print "func.f_code.co_filename is %s" % func.f_code.co_filename
        #print "func.f_lineno is %s" % func.f_lineno
        filename = os.path.basename(func.f_code.co_filename)
        lineno = func.f_lineno
        funcname = func.f_code.co_name
        linemessage = '%s:%s - %s() ] %s' % (filename, lineno, funcname[:15], message)
        self.logger.warning(linemessage)

    def error(self, message):
        func = inspect.currentframe().f_back
        #print "func.f_code.co_name is %s" % func.f_code.co_name
        #print "func.f_code.co_filename is %s" % func.f_code.co_filename
        #print "func.f_lineno is %s" % func.f_lineno
        filename = os.path.basename(func.f_code.co_filename)
        lineno = func.f_lineno
        funcname = func.f_code.co_name
        linemessage = '%s:%s - %s() ] %s' % (filename, lineno, funcname[:15], message)
        self.logger.error(linemessage)

