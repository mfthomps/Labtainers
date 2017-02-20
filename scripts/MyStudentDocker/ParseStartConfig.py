#!/usr/bin/env python

import os
import sys

container_keywords={"user", "image_name"}

class ParseStartConfig():
    def __init__(self, fname, labname, caller, version=2):
        self.version = int(version) # in case this is passed in from a string somewhere
        self.containers = {} # dictionary of containers
        self.conf = {  # dictionary of config settings
                               "labname": labname,
                               "caller": caller,
                               "host_home_xfer": None,
                               "lab_master_seed": None
                             } 

        self.container_name="" # Name of container
        self.container_image="" # Name of container image
        self.container_user="" # Name of user
        self.host_home_xfer="" # HOST_HOME_XFER - directory to transfer artifact to/from containers
        self.lab_master_seed="" # LAB_MASTER_SEED - this is the master seed string for to this laboratory
        if caller != "student" and caller != "instructor":
            sys.stderr.write("Unexpected caller of ParseStartConfig module!\n")
            sys.exit(1)
        if not os.path.exists(fname):
            sys.stderr.write("Config file %s does not exists!\n" % fname)
            sys.exit(1)
        if self.version == 1:
            print "config version 1"
            self.do_parsing(fname, labname, caller)
        elif self.version == 2:
            print "config version 2"
            self.get_configs(fname)
            self.validate()
            self.finalize()
        else:
            sys.stderr.write("Uknown version. I die.\n")
            sys.exit(1)

    def get_configs(self, fname):
        """Reads the new config format. There is basically no format validation so 
           this accidentally supports a much more flexible format right now, which 
           is bad. It does check for unknown config options, which is good. The main
           advantage is that I think the parsing method should be easy to extend."""
        nickname = "default"
        with open(fname, "r") as f:
            for line in f:
                linestrip = line.rstrip()
                if not linestrip or linestrip.startswith("#"):
                  continue
                key, val = linestrip.split()    
                key = key.lower()
                if key == "container":
                    self.containers[val] = {}
                    nickname = val 
                elif key in container_keywords:
                    self.containers[nickname][key.lower()] = val
                elif key in self.conf.keys():
                    self.conf[key] = val
                else:
                    sys.stderr.write("Fatal. Can't understand line: %s" % line)
                    sys.exit(-1)
        
    def validate(self):
        """ Checks to make sure we have all the info we need from the user."""
        if (self.conf["host_home_xfer"] == None):
            sys.stderr.write("ERROR: Missing host_home_xfer in start.config!\n")
            sys.exit(-1)
        
        if (self.conf["caller"] == "student"):
           if (self.conf["lab_master_seed"] == None):
               sys.stderr.write("ERROR: Missing lab_master_seed in start.config!\n")
               sys.exit(-1)

        for container in self.containers.values():
            if "user" not in container.keys():
                sys.stderr.write("ERROR: No user found for container %s in "
                                 "start.config!\n" % container["nickname"])
                sys.exit(-1)

    def finalize(self):
        """Combines info provided by user with what we already know about the
           lab to get the final settings we want."""
        # renaming for brevity
        caller = self.conf["caller"]
        raw_xfer = self.conf["host_home_xfer"] 
        raw_seed = self.conf["lab_master_seed"] 
        labname  = self.conf["labname"]

        # fixing up global parameters
        self.conf["host_home_xfer"] = os.path.join(raw_xfer,labname)
        self.conf["lab_master_seed"] = labname + raw_seed

        # fixing up container parameters
        for nickname in self.containers.keys():
            name = nickname
            if name == "default": name = ""
            full  = labname + name + "." + caller 
            image = labname + name + ":" + caller
            if "full_name" not in self.containers[nickname].keys():
               self.containers[nickname]["full_name"] = full
            if "image_name" not in self.containers[nickname].keys():
               self.containers[nickname]["image_name"] = image 

    def show_current_settings(self):
        if self.version != 2: return
        bar = "="*80
        print bar
        print("Global configuration settings:")
        print bar
        for key, val in self.conf.items():
            print "\t" + str(key) + ": " + str(val)
        print "\n"+bar
        print("Container configuration settings:")
        print bar
        for nickname, container in self.containers.items():
            print "nickname: " + nickname 
            for key, val in container.items():
                print "\t" + str(key) + ": " + str(val)
            print ""
            

    def do_parsing(self, fname, labname, caller):
        # caller must be "student" or "instructor"
       
        #print "ParseStartConfig for %s" % labname
        # Make sure start.config configuration file exists
        configfile = open(fname)
        configfilelines = configfile.readlines()
        configfile.close()
    
        container_name_found = False
        container_image_name_found = False
        container_user_found = False
        host_home_found = False
        if caller == "student":
            lab_master_seed_found = False
        else:
            # Don't need lab master seed for instructor
            lab_master_seed_found = True
        for line in configfilelines:
            linestrip = line.rstrip()
            if linestrip:
                if not linestrip.startswith('#'):
                    (key, value) = linestrip.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # replace $lab with labname
                    newvalue = value.replace('$lab', labname)
                    # replace '"' with ''
                    newvalue = newvalue.replace('"', '')
                    #print "Key is (%s) with value (%s)" % (key, newvalue)
                    if key == "CONTAINER_NAME":
                        self.container_name = newvalue
                        # DO NOT allow '=' in container name
                        if '=' in self.container_name:
                            sys.stderr.write('Character "=" is not allowed in container name (%s)\n' % newvalue)
                            sys.exit(1)
                        container_name_found = True
                    elif key == "CONTAINER_IMAGE":
                        self.container_image = newvalue
                        container_image_found = True
                    elif key == "CONTAINER_USER":
                        self.container_user = newvalue
                        container_user_found = True
                    elif key == "HOST_HOME_XFER":
                        self.host_home_xfer = newvalue
                        host_home_xfer_found = True
                    elif key == "LAB_MASTER_SEED":
                        self.lab_master_seed = newvalue
                        lab_master_seed_found = True
                    else:
                        sys.stderr.write("ERROR: Unexpected config item in start.config!\n")
                        sys.exit(1)
            #else:
            #    print "Skipping empty linestrip is (%s)" % linestrip
    
        if not (container_name_found and
                container_image_found and
                container_user_found and
                host_home_xfer_found and
                lab_master_seed_found):
            sys.stderr.write("ERROR: Missing config item in start.config!\n")
            sys.exit(1)
    

if __name__ == '__main__':
    start_config = ParseStartConfig(*sys.argv[1:])
    start_config.show_current_settings()
