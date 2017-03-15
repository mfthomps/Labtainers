#!/usr/bin/env python

import os
import sys
from netaddr import *
import re

def isalphadashscore(name):
    # check name - alphanumeric,dash,underscore
    return re.match(r'^[a-zA-Z0-9_-]*$', name)

class ParseStartConfig():
    def __init__(self, fname, labname, caller):
        self.containers = {} # dictionary of containers
        self.subnets    = {} # dictionary of subnets 
        self.labname = labname
        self.caller = caller
        self.host_home_xfer= "" # HOST_HOME_XFER - directory to transfer artifact to/from containers
        self.lab_master_seed= None # LAB_MASTER_SEED - this is the master seed string for to this laboratory
        self.grade_container = None # GRADE_CONTAINER - this is where the instructor performs the grading

        if not os.path.exists(fname):
            sys.stderr.write("Config file %s does not exists!\n" % fname)
            sys.exit(1)

        self.get_configs(fname)
        self.finalize()
        self.validate()

    class Container():
        def __init__(self, name):
            self.name       = name
            self.terminals  = 2
            self.user       = "user"
            self.image_name = ""
            self.full_name  = ""
            self.container_nets = {} #dictionary of name and ip addr 

        def add_net(self, name, ipaddr):
            self.container_nets[name] = ipaddr

        def validate(self, valid_networks=set()):
            self.terminals = int(self.terminals) #replace with something smarter
          
            if '=' in self.name: # TODO: do we still need this?
                sys.stderr.write('Character "=" is not allowed in container name (%s)' % self.name)
                exit(1)
            for name, addr in self.container_nets.items():
                if name not in valid_networks:
                    sys.stderr.write('Container %s cannot be added to undefined network %s' % (self.full_name, name))
                    exit(1)
                try:
                    IPAddress(addr)
                except:
                    sys.stderr.write('bad ip addr %s in \t%s' % (addr, name))
                    exit(1)

    class Subnet():
        def __init__(self, name):
            self.name   = name
            self.mask = 0
            self.gateway = 0

        def validate(self):
            if not isalphadashscore(self.name):
                sys.stderr.write('bad subnet name %s in for network %s' % (self.name, self.id))
                exit(1)
            try:
                IPNetwork(self.mask)
            except:
                sys.stderr.write('bad ip subnet %s for network %s' % (self.mask, self.id))
                exit(1)
            if not IPAddress(self.gateway) in IPNetwork(self.mask):
                sys.stderr.write('Gateway IP (%s) not in subnet for SUBNET line(%s)!\n' % 
                    (self.gateway, self.mask))
                exit(1)

    def add_if_new(self, name, location, thing):
        if name in location:
            sys.stderr.write("Fatal. '%s' already defined." % name)
            exit(1)
        location[name] = thing

    def get_configs(self, fname):
        """Reads the new config format. There is basically no format validation so 
           this accidentally supports a much more flexible format right now, which 
           is bad. It does check for unknown config options, which is good. The main
           advantage is that I think the parsing method should be easy to extend."""
        active      = None
        defaults_ok = {"network","container", "global_settings"}
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
                    sys.stderr.write("Fatal. Missing value for: %s" % line)
                    exit(1)

                if key == "global_settings":
                    active = self
                elif key == "network":
                    self.add_if_new(val, self.subnets, self.Subnet(val))
                    active = self.subnets[val]
                elif key == "container":
                    self.add_if_new(val, self.containers, self.Container(val))
                    active = self.containers[val]
                elif hasattr(active, key):
                    setattr(active, key, val) 
                else:
                    try:
                        active.add_net(key,val)
                    except:
                        sys.stderr.write("Fatal. Can't understand config setting: %s" % line)
                        exit(1)

    def validate(self):
        """ Checks to make sure we have all the info we need from the user."""
        if self.caller != "student" and self.caller != "instructor":
            sys.stderr.write("Unexpected caller of ParseStartConfig module!\n")
            exit(1)

        if not self.host_home_xfer:
            sys.stderr.write("ERROR: Missing host_home_xfer in start.config!\n")
            exit(1)
        
        if (self.caller == "student"):
           if not self.lab_master_seed:
               sys.stderr.write("ERROR: Missing lab_master_seed in start.config!\n")
               exit(1)

        if not self.grade_container:
            sys.stderr.write("ERROR: Missing grade_container in start.config!\n")
            exit(1)

        for subnet in self.subnets.values():
            subnet.validate()

        for container in self.containers.values():
            container.validate(self.subnets.keys())


    def finalize(self):
        """Combines info provided by user with what we already know about the
           lab to get the final settings we want."""
        # fixing up global parameters
        self.host_home_xfer = os.path.join(self.host_home_xfer,self.labname)
        self.lab_master_seed = self.labname + self.lab_master_seed
        if self.grade_container == "default":
            self.grade_container = self.labname + "." + self.caller 
        else:
            self.grade_container = self.labname + "." + self.grade_container + "." + self.caller 

        # fixing up container parameters
        for name in self.containers:
            if name == "default": namestr = ""
            else:
                namestr = "." + name
            full  = self.labname + namestr + "." + self.caller 
            image = self.labname + namestr + ":" + self.caller
            if self.containers[name].full_name == "":
               self.containers[name].full_name = full
            if self.containers[name].image_name == "":
               self.containers[name].image_name = image 

    def show_current_settings(self):
        bar = "="*80
        print bar
        print("Global configuration settings:")
        print bar
        for key, val in self.__dict__.items():
            if type(val) == type({}): val = len(val)
            print "\t" + str(key) + ": " + str(val)
        print "\n"+bar
        print("Network configuration settings:")
        print bar
        for name, network in self.subnets.items():
            print "name: " + name 
            for key, val in network.__dict__.items():
                if type(val) == type({}): val = len(val)
                print "\t" + str(key) + ": " + str(val)
            print ""
        print "\n"+bar
        print("Container configuration settings:")
        print bar
        for name, container in self.containers.items():
            print "name: " + name 
            for key, val in container.__dict__.items():
                if type(val) == type({}): val = len(val)
                print "\t" + str(key) + ": " + str(val)
            print ""
             
if __name__ == '__main__':
    start_config = ParseStartConfig(*sys.argv[1:])
    start_config.show_current_settings()
