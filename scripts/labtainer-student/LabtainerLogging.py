#!/usr/bin/env python
'''
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
'''

import inspect
import logging
import os
import sys
import re

import MyGlobal

class LabtainerLogging():
    def __init__(self, logfilename, loglevel, logname):
        #print "filename is (%s)" % logfilename
        #print "loglevel is (%d)" % loglevel
        #print "logname is (%s)" % logname
        self.logger = logging.getLogger(logname)
        LOGFORMAT = '[%(asctime)s %(message)s'
        logging.basicConfig(filename=logfilename, level=loglevel, format=LOGFORMAT)

    def DEBUG(self, message):
        func = inspect.currentframe().f_back
        #print "func.f_code.co_name is %s" % func.f_code.co_name
        #print "func.f_code.co_filename is %s" % func.f_code.co_filename
        #print "func.f_lineno is %s" % func.f_lineno
        filename = os.path.basename(func.f_code.co_filename)
        lineno = func.f_lineno
        funcname = func.f_code.co_name
        linemessage = '%s:%s - %s() ] %s' % (filename, lineno, funcname[:15], message)
        self.logger.debug(linemessage)

    def INFO(self, message):
        func = inspect.currentframe().f_back
        #print "func.f_code.co_name is %s" % func.f_code.co_name
        #print "func.f_code.co_filename is %s" % func.f_code.co_filename
        #print "func.f_lineno is %s" % func.f_lineno
        filename = os.path.basename(func.f_code.co_filename)
        lineno = func.f_lineno
        funcname = func.f_code.co_name
        linemessage = '%s:%s - %s() ] %s' % (filename, lineno, funcname[:15], message)
        self.logger.info(linemessage)

    def WARNING(self, message):
        func = inspect.currentframe().f_back
        #print "func.f_code.co_name is %s" % func.f_code.co_name
        #print "func.f_code.co_filename is %s" % func.f_code.co_filename
        #print "func.f_lineno is %s" % func.f_lineno
        filename = os.path.basename(func.f_code.co_filename)
        lineno = func.f_lineno
        funcname = func.f_code.co_name
        linemessage = '%s:%s - %s() ] %s' % (filename, lineno, funcname[:15], message)
        self.logger.warning(linemessage)

    def ERROR(self, message):
        func = inspect.currentframe().f_back
        #print "func.f_code.co_name is %s" % func.f_code.co_name
        #print "func.f_code.co_filename is %s" % func.f_code.co_filename
        #print "func.f_lineno is %s" % func.f_lineno
        filename = os.path.basename(func.f_code.co_filename)
        lineno = func.f_lineno
        funcname = func.f_code.co_name
        linemessage = '%s:%s - %s() ] %s' % (filename, lineno, funcname[:15], message)
        self.logger.error(linemessage)

