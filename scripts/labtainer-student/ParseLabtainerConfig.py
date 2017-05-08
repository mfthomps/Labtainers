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

import os
import sys
import LabtainerLogging
import Labtainer

class ParseLabtainerConfig():
    def __init__(self, fname, labname):
        self.labname = labname
        self.host_home_xfer= "" # HOST_HOME_XFER - directory to transfer artifact to/from containers
        self.testsets_root= None # TESTSETS_ROOT - regression test root

        if not os.path.exists(fname):
            Labtainer.logger.ERROR("Config file %s does not exists!\n" % fname)
            sys.exit(1)

        self.get_configs(fname)
        self.finalize()
        self.validate()

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
                    Labtainer.logger.ERROR("Fatal. Missing value for: %s" % line)
                    exit(1)

                if key == "global_settings":
                    active = self
                elif hasattr(active, key):
                    setattr(active, key, val) 
                else:
                    Labtainer.logger.ERROR("Fatal. Can't understand config setting: %s" % line)
                    exit(1)

    def validate(self):
        """ Checks to make sure we have all the info we need from the user."""
        if not self.host_home_xfer:
            Labtainer.logger.ERROR("Missing host_home_xfer in labtainer.config!\n")
            exit(1)
        if not self.testsets_root:
            Labtainer.logger.ERROR("Missing testsets_root in labtainer.config!\n")
            exit(1)
        
    def finalize(self):
        """Combines info provided by user with what we already know about the
           lab to get the final settings we want."""
        # fixing up global parameters
        self.host_home_xfer = os.path.join(self.host_home_xfer,self.labname)
        self.testsets_root = os.path.join(os.path.abspath(self.testsets_root), self.labname)

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
