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

import logging
import os
import sys
import LabtainerLogging

class ParseLabtainerConfig():
    def __init__(self, fname, logger):
        self.host_home_xfer= "" # HOST_HOME_XFER - directory to transfer artifact to/from containers
        self.testsets_root= None # TESTSETS_ROOT - regression test root
        self.file_log_level= "" # FILE_LOG_LEVEL - level to log to file
        self.console_log_level= "" # CONSOLE_LOG_LEVEL - level to log to console
        if logger != None:
            self.logger = logger
        else:
            self.logger = None
        if not os.path.exists(fname):
            self.mylog("Config file %s does not exists!\n" % fname)
            sys.exit(1)

        self.get_configs(fname)
        self.finalize()
        self.validate()

    def mylog(self, message):
        if self.logger != None:
            self.logger.ERROR(message)
        else:
            sys.stderr.write(message)


    def get_configs(self, fname):
        """Reads the new config format. There is basically no format validation so 
           this accidentally supports a much more flexible format right now, which 
           is bad. It does check for unknown config options, which is good. The main
           advantage is that I think the parsing method should be easy to extend."""
        active      = None
        defaults_ok = {"global_settings"}
        with open(fname, "r") as f:
            for line in f:
                linestrip = line.strip()
                if not linestrip or linestrip.startswith("#"):
                    continue
                keyval = linestrip.split()    
                key = keyval[0].lower()
                if len(keyval) > 1:
                    val = keyval[1].lower()
                elif key in defaults_ok:
                    val = "default"
                else:
                    self.mylog("Fatal. Missing value for: %s" % line)
                    exit(1)

                if key == "global_settings":
                    active = self
                elif hasattr(active, key):
                    setattr(active, key, val) 
                else:
                    self.mylog("Fatal. Can't understand config setting: %s" % line)
                    exit(1)

    def validate(self):
        """ Checks to make sure we have all the info we need from the user."""
        if not self.host_home_xfer:
            self.mylog("Missing host_home_xfer in labtainer.config!\n")
            exit(1)
        if not self.testsets_root:
            self.mylog("Missing testsets_root in labtainer.config!\n")
            exit(1)
        if not self.file_log_level:
            self.mylog("Missing file_log_level in labtainer.config!\n")
            exit(1)
        if not self.console_log_level:
            self.mylog("Missing console_log_level in labtainer.config!\n")
            exit(1)
        
    def finalize(self):
        """Combines info provided by user with what we already know about the
           lab to get the final settings we want."""
        # fixing up global parameters
        valid_log_levels = {"debug", "info", "warning", "error"}
        if self.file_log_level not in valid_log_levels:
            self.mylog("Invalid file_log_level (%s) in labtainer.config!\n" % self.file_log_level)
            exit(1)
        if self.console_log_level not in valid_log_levels:
            self.mylog("Invalid console_log_level (%s) in labtainer.config!\n" % self.console_log_level)
            exit(1)
        logging_levels = {'debug' : logging.DEBUG,
                          'info' : logging.INFO,
                          'warning' : logging.WARNING,
                          'error' : logging.ERROR}
        self.file_log_level = logging_levels[self.file_log_level]
        self.console_log_level = logging_levels[self.console_log_level]


    def show_current_settings(self):
        bar = "="*80
        print bar
        print("Global configuration settings:")
        print bar
        for key, val in self.__dict__.items():
            if type(val) == type({}): val = len(val)
            print "\t" + str(key) + ": " + str(val)
        print "\n"+bar
             
if __name__ == '__main__':
    labtainer_config = ParseLabtainerConfig(*sys.argv[1:])
    labtainer_config.show_current_settings()
