#!/usr/bin/env python

import os
import sys

class ParseStartConfig():
    def __init__(self, fname, labname):
        self.container_name="" # Name of container
        self.container_image="" # Name of container image
        self.container_user="" # Name of user
        self.host_home_xfer="" # HOST_HOME_XFER - directory to transfer artifact to/from containers
        self.lab_master_seed="" # LAB_MASTER_SEED - this is the master seed string for to this laboratory

        #print "ParseStartConfig for %s" % labname
        # Make sure start.config configuration file exists
        if not os.path.exists(fname):
            sys.stderr.write("Config file %s does not exists!\n" % fname)
            sys.exit(1)
        configfile = open(fname)
        configfilelines = configfile.readlines()
        configfile.close()
    
        container_name_found = False
        container_image_name_found = False
        container_user_found = False
        host_home_found = False
        lab_master_seed_found = False
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
    start_config = ParseStartConfig(sys.argv[1], sys.arg[2])
