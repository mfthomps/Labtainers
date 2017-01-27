#!/usr/bin/env python

# Filename: start.py
# Description:
# This is the start script to be run by the student.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
# 2. If the lab has multiple containers and/or multi-home
#    networking, then <labname>.network file is necessary
#

import glob
import json
import md5
import os
import re
import subprocess
import sys
import time
import zipfile
from netaddr import *

# Error code returned by docker inspect
SUCCESS=0
FAILURE=1

class MyContainerLine(object):
    """ ContainerLine - container_name, container_image_name, num_terminal, network_subnets """
    container_name = ""
    container_image_name = ""
    num_terminal = ""
    network_subnets = {}

    def container_dict(object):
        return object.__dict__

    def __init__(self, container_name, container_image_name, num_terminal, network_subnets):
        self.container_name = container_name
        self.container_image_name = container_image_name
        self.num_terminal = num_terminal
        self.network_subnets = network_subnets

# Networks
networklist = {}

# Containers
containerslist = {}

container_name="" # Name of container
container_image="" # Name of container image
container_user="" # Name of user
host_home_xfer="" # HOST_HOME_XFER - directory to transfer artifact to/from containers
lab_master_seed="" # LAB_MASTER_SEED - this is the master seed string for to this laboratory

def isalphadashscore(name):
    # check name - alphanumeric,dash,underscore
    if re.match(r'^[a-zA-Z0-9_-]*$', name):
        return True
    else:
        return False

# get docker0 IP address
def getDocker0IPAddr():
    command="ifconfig docker0 | awk '/inet addr:/ {print $2}' | sed 's/addr://'"
    #print "Command to execute is (%s)" % command
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    result = child.stdout.read().strip()
    #print "Result of subprocess.Popen getDocket0IPAddr is %s" % result
    return result

# Parameterize my_container_name container
def ParameterizeMyContainer(mycontainer_name, lab_instance_seed, user_email, labname):
    #print "About to call parameterize.sh with LAB_INSTANCE_SEED = (%s)" % lab_instance_seed
    command = 'docker exec -it %s script -q -c "/home/ubuntu/.local/bin/parameterize.sh %s %s %s" /dev/null' % (mycontainer_name, lab_instance_seed, user_email, labname)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call ParameterizeMyContainer is %s" % result
    return result

# Start my_container_name container
def StartMyContainer(mycontainer_name):
    command = "docker start %s 2> /dev/null" % mycontainer_name
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call StartMyContainer is %s" % result
    return result

# Check to see if my_container_name container has been created or not
def IsContainerCreated(mycontainer_name):
    command = "docker inspect -f {{.Created}} %s 2> /dev/null" % mycontainer_name
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call IsContainerCreated is %s" % result
    return result

def ConnectNetworkToContainer(mycontainer_name, mysubnet_name, mysubnet_ip, mygateway_ip):
    #print "Connecting more network subnet to container %s" % mycontainer_name
    if mygateway_ip == "":
        command = "docker network connect --ip=%s %s %s 2> /dev/null" % (mysubnet_ip, mysubnet_name, mycontainer_name)
    else:
        command = "docker network connect --ip=%s --gateway=%s %s %s 2> /dev/null" % (mysubnet_ip, mygateway_ip, mysubnet_name, mycontainer_name)
    print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call ConnectNetworkToContainer is %s" % result
    return result

def CreateSingleContainerNonDefault(mycontainer_name, mycontainer_image_name,
          mysubnet_name, mysubnet_ip):
    #print "Create Single Container with non-default networking"
    docker0_IPAddr = getDocker0IPAddr()
    #print "getDockerIPAddr result (%s)" % docker0_IPAddr
    createsinglecommand = "docker create -t --network=%s --ip=%s --privileged --add-host my_host:%s --name=%s %s bash" % (mysubnet_name, mysubnet_ip, docker0_IPAddr, mycontainer_name, mycontainer_image_name)
    print "Command to execute is (%s)" % createsinglecommand
    result = subprocess.call(createsinglecommand, shell=True)
    #print "Result of subprocess.call CreateSingleContainerNonDefault is %s" % result
    return result

def CreateSingleContainerDefault():
    #print "Create Single Container with default networking"
    docker0_IPAddr = getDocker0IPAddr()
    #print "getDockerIPAddr result (%s)" % docker0_IPAddr
    createsinglecommand = "docker create -t --privileged --add-host my_host:%s --name=%s %s bash" % (docker0_IPAddr, container_name, container_image)
    print "Command to execute is (%s)" % createsinglecommand
    result = subprocess.call(createsinglecommand, shell=True)
    #print "Result of subprocess.call CreateSingleContainerDefault is %s" % result
    return result

def DoSingle(mycwd, labname):
    #print "Do Single Container with default networking"
    haveContainer = IsContainerCreated(container_name)
    #print "IsContainerCreated result (%s)" % haveContainer

    # Set need_seeds=False first
    need_seeds=False

    # IsContainerCreated returned FAILURE if container does not exists
    if haveContainer == FAILURE:
        # Container does not exist, create the container
        containerCreated = CreateSingleContainerDefault()
        #print "CreateSingleContainerDefault result (%s)" % containerCreated
        # If we just create it, then set need_seeds=True
        need_seeds=True
        # Give the container some time -- just in case
        time.sleep(3)

    # Check again - 
    haveContainer = IsContainerCreated(container_name)
    #print "IsContainerCreated result (%s)" % haveContainer

    # IsContainerCreated returned FAILURE if container does not exists
    if haveContainer == FAILURE:
        sys.stderr.write("ERROR: DoSingle Container %s still not created!\n" % container_name)
        sys.exit(1)
    else:
        # Start the container
        StartMyContainer(container_name)

    # If the container is just created, prompt user's e-mail
    # then parameterize the container
    if need_seeds:
        # Prompt user for e-mail address
        user_email = raw_input("Please enter your e-mail address: ")
        # Create hash using LAB_MASTER_SEED concatenated with user's e-mail
        # LAB_MASTER_SEED is per laboratory - specified in start.config
        string_to_be_hashed = '%s:%s' % (lab_master_seed, user_email)
        mymd5 = md5.new()
        mymd5.update(string_to_be_hashed)
        mymd5_hex_string = mymd5.hexdigest()
        #print mymd5_hex_string

        parameterize_result = ParameterizeMyContainer(container_name, mymd5_hex_string,
                                                      user_email, labname)
        if parameterize_result == FAILURE:
            sys.stderr.write("ERROR: Failed to parameterize lab container %s!\n" % container_name)
            sys.exit(1)

    # Reach here - Everything is OK - spawn two terminals by default
    spawn_command = "gnome-terminal -x docker exec -it %s bash -l &" % container_name
    os.system(spawn_command)
    os.system(spawn_command)

    return 0

# Create SUBNETS
def CreateSubnets():
    #print "Inside CreateSubnets"
    for (subnet_name, subnet_network_mask) in networklist.iteritems():
        #print "subnet_name is %s" % subnet_name
        #print "subnet_network_mask is %s" % subnet_network_mask

        command = "docker network inspect %s > /dev/null" % subnet_name
        #print "Command to execute is (%s)" % command
        inspect_result = subprocess.call(command, shell=True)
        #print "Result of subprocess.call CreateSubnets docker network inspect is %s" % inspect_result
        if inspect_result == FAILURE:
            # Fail means does not exist - then we can create
            command = "docker network create -d bridge --subnet %s %s 2> /dev/null" % (subnet_network_mask, subnet_name)
            #print "Command to execute is (%s)" % command
            create_result = subprocess.call(command, shell=True)
            #print "Result of subprocess.call CreateSubnets docker network create is %s" % create_result
            if create_result == FAILURE:
                sys.stderr.write("ERROR: Failed to create %s subnet at %s!\n" % (subnet_name, subnet_network_mask))
                sys.exit(1)
        else:
            print "Already exists! Not creating %s subnet at %s!\n" % (subnet_name, subnet_network_mask)
        

def ParseNetworkConfig(mycwd, labname):
    #print "ParseNetworkConfig for %s" % labname
    networkfilename = '%s/%s.network' % (mycwd, labname)
    # At this point we know <labname>.network configuration file exists
    networkfile = open(networkfilename)
    for line in networkfile:
        linestrip = line.rstrip()
        if linestrip:
            if not linestrip.startswith('#'):
                # if startswith 'NETWORK' -- these are subnets
                # the expected format : NETWORK <SUBNET_NAME> <SUBNET_NETWORK_MASK>
                if linestrip.startswith('NETWORK'):
                    subnettokens = linestrip.split()
                    if len(subnettokens) != 3:
                        sys.stderr.write("ERROR: Invalid SUBNET line format (%s)!\n" % linestrip)
                        sys.exit(1)
                    subnet_name = subnettokens[1].strip()
                    subnet_network_mask = subnettokens[2].strip()
                    # Valid subnet_name - alphanumeric,dash,underscore
                    if not isalphadashscore(subnet_name):
                        sys.stderr.write("ERROR: Invalid subnet name in SUBNET line (%s)!\n" % linestrip)
                        sys.exit(1)
                    try:
                        IPNetwork(subnet_network_mask)
                    except core.AddrFormatError:
                        sys.stderr.write("ERROR: Invalid subnet_network_mask in SUBNET line (%s)!\n" % linestrip)
                        sys.exit(1)
                    networklist[subnet_name] = subnet_network_mask

                # if startswith 'CONTAINER' -- these are containers
                if linestrip.startswith('CONTAINER'):
                    # the expected format for the CONTAINER first line is:
                    # CONTAINER <CONTAINER_NAME> <CONTAINER_IMAGE_NAME> [<TERM>]
                    # <TERM> - representing the number of terminal to spawn is optional
                    container1line = linestrip.split()
                    #print "Number of Container line token is %d" % len(container1line)
                    if len(container1line) != 3 and len(container1line) != 4:
                        sys.stderr.write("ERROR: Invalid CONTAINER line format (%s)!\n" % linestrip)
                        sys.exit(1)
                    mycontainer_name = container1line[1].strip()
                    mycontainer_image_name = container1line[2].strip()
                    if len(container1line) == 2:
                        num_term = 0
                    else:
                        try:
                            int(container1line[3].strip())
                        except ValueError:
                            sys.stderr.write("ERROR: Invalid terminal no in CONTAINER line (%s)!\n" % linestrip)
                            sys.exit(1)
                        num_term = int(container1line[3].strip())

                    # Container name and Container image name is not restricted to alphanumeric,dash,underscore
                    ###### Valid container_name - alphanumeric,dash,underscore
                    #####if not isalphadashscore(mycontainer_name):
                    #####    sys.stderr.write("ERROR: Invalid container name in CONTAINER line (%s)!\n" % linestrip)
                    #####    sys.exit(1)
                    ###### Valid container_image_name - alphanumeric,dash,underscore
                    #####if not isalphadashscore(mycontainer_image_name):
                    #####    sys.stderr.write("ERROR: Invalid container image name in CONTAINER line (%s)!\n" % linestrip)
                    #####    sys.exit(1)

                    # Process subsequent line until empty line
                    try:
                        next_line = networkfile.next().strip()
                    except:
                        sys.stderr.write("ERROR: No network line after CONTAINER line (%s)!\n" % linestrip)
                        sys.exit(1)
                    mynetwork_subnet_list = []
                    #print "Next line after container is (%s)" % next_line
                    while (next_line):
                        # the expected format of line after CONTAINER is:
                        # + <SUBNET_NAME> <IPADDR> [GATEWAY]>
                        mynetwork_subnet_tokens = next_line.split()
                        if len(mynetwork_subnet_tokens) != 3 and len(mynetwork_subnet_tokens) != 4:
                            sys.stderr.write("ERROR: Invalid CONTAINER network line format (%s)!\n" % next_line)
                            sys.exit(1)
                        # Found a 'CONTAINER' line next before empty line
                        if next_line.startswith('CONTAINER'):
                            sys.stderr.write("ERROR: Please separate CONTAINER lines with empty line(%s)!\n" % next_line)
                            sys.exit(1)
                        # First token must be '+'
                        if mynetwork_subnet_tokens[0] != '+':
                            sys.stderr.write("ERROR: Missing '+' in CONTAINER network line(%s)!\n" % next_line)
                            sys.exit(1)
                        mysubnet_name = mynetwork_subnet_tokens[1]
                        # Subnet name must be defined
                        if not mysubnet_name in networklist:
                            sys.stderr.write("ERROR: Unknown subnet name in CONTAINER network line(%s)!\n" % next_line)
                            sys.exit(1)
                        mysubnet_ip = mynetwork_subnet_tokens[2]
                        if not IPAddress(mysubnet_ip) in IPNetwork(networklist[mysubnet_name]):
                            sys.stderr.write("ERROR: IP address not in subnet for CONTAINER network line(%s)!\n" % next_line)
                            sys.exit(1)
                        if len(mynetwork_subnet_tokens) == 3:
                            mygateway_ip = ""
                        else:
                            mygateway_ip = mynetwork_subnet_tokens[3]
                            try:
                                IPAddress(mygateway_ip)
                            except:
                                sys.stderr.write("ERROR: Invalid Gateway IP address for CONTAINER network line(%s)!\n" % next_line)
                                sys.exit(1)

                        # If get to here, the current line is OK, store it
                        mynetwork_subnet_list.append('%s %s %s' % (mysubnet_name, mysubnet_ip, mygateway_ip))

                        # Get the next line
                        try:
                            next_line = networkfile.next().strip()
                        except:
                            # EOF? - break while loop
                            next_line = ""
                        #print "Next line is (%s)" % next_line

                    if mynetwork_subnet_list == []:
                        sys.stderr.write("ERROR: Must have at least one subnet for CONTAINER line(%s)!\n" % linestrip)
                        sys.exit(1)

                    #print "Container name is %s" % mycontainer_name
                    #print "Container image name is %s" % mycontainer_image_name
                    #print "Current CONTAINER line network subnet list is "
                    #print mynetwork_subnet_list

                    # Store a good Container line
                    containerslist[mycontainer_name] = MyContainerLine(mycontainer_name, mycontainer_image_name,
                                                                     num_term, mynetwork_subnet_list)

    networkfile.close()

def DoMultiple(mycwd, labname):
    global container_name
    global container_image
    global container_user
    global host_home_xfer
    global lab_master_seed
    #print "Multiple Containers and/or multi-home networking"
    docker0_IPAddr = getDocker0IPAddr()
    #print "getDockerIPAddr result (%s)" % docker0_IPAddr
    ParseNetworkConfig(mycwd, labname)
    #print "After ParseNetworkConfig"
    #print networklist
    #for (container_name, containerline) in containerslist.iteritems():
    #    print containerline.container_dict()

    # Create SUBNETS
    CreateSubnets()

    for (container_name, containerline) in containerslist.iteritems():
        #print containerline.container_dict()
        mycontainer_name = containerline.container_name
        mycontainer_image_name = containerline.container_image_name

        haveContainer = IsContainerCreated(container_name)
        #print "IsContainerCreated result (%s)" % haveContainer

        # Set need_seeds=False first
        need_seeds=False

        # IsContainerCreated returned FAILURE if container does not exists
        if haveContainer == FAILURE:
            first_subnet_for_container = True
            for eachsubnet in containerline.network_subnets:
                #print "Network subnet is (%s)" % eachsubnet
                mynetwork_subnet_tokens = eachsubnet.split()
                mysubnet_name = mynetwork_subnet_tokens[0]
                #print "My subnet name is %s" % mysubnet_name
                mysubnet_ip = mynetwork_subnet_tokens[1]
                #print "My subnet ip is %s" % mysubnet_ip
                if len(mynetwork_subnet_tokens) == 2:
                    mygateway_ip = ""
                else:
                    mygateway_ip = mynetwork_subnet_tokens[2]

                # First subnet must be part of docker create
                if first_subnet_for_container:
                    first_subnet_for_container = False
                    # Container does not exist, create the container
                    # Use CreateSingleContainerNonDefault()
                    #print "My subnet name is %s" % mysubnet_name
                    #print "My subnet ip is %s" % mysubnet_ip
                    containerCreated = CreateSingleContainerNonDefault(mycontainer_name, mycontainer_image_name,
                                             mysubnet_name, mysubnet_ip)
                    #print "CreateSingleContainerNonDefault result (%s)" % containerCreated
                    # This is a hack - can't set gateway in the create
                    connectNetworkResult = ConnectNetworkToContainer(mycontainer_name, mysubnet_name,
                                                  mysubnet_ip, mygateway_ip)
                    # If we just create it, then set need_seeds=True
                    need_seeds=True
                    # Give the container some time -- just in case
                    time.sleep(3)
                else:
                # Subsequent subnet must use docker network connect
                    #print "My subnet name is %s" % mysubnet_name
                    #print "My subnet ip is %s" % mysubnet_ip
                    connectNetworkResult = ConnectNetworkToContainer(mycontainer_name, mysubnet_name,
                                                  mysubnet_ip, mygateway_ip)

        # Check again - 
        haveContainer = IsContainerCreated(container_name)
        #print "IsContainerCreated result (%s)" % haveContainer

        # IsContainerCreated returned FAILURE if container does not exists
        if haveContainer == FAILURE:
            sys.stderr.write("ERROR: DoMultiple Container %s still not created!\n" % container_name)
            sys.exit(1)
        else:
            # Start the container
            StartMyContainer(container_name)

        # If the container is just created, prompt user's e-mail
        # then parameterize the container
        if need_seeds:
            # Prompt user for e-mail address
            user_email = raw_input("Please enter your e-mail address: ")
            # Create hash using LAB_MASTER_SEED concatenated with user's e-mail
            # LAB_MASTER_SEED is per laboratory - specified in start.config
            string_to_be_hashed = '%s:%s' % (lab_master_seed, user_email)
            mymd5 = md5.new()
            mymd5.update(string_to_be_hashed)
            mymd5_hex_string = mymd5.hexdigest()
            #print mymd5_hex_string
    
            parameterize_result = ParameterizeMyContainer(container_name, mymd5_hex_string,
                                                          user_email, labname)
            if parameterize_result == FAILURE:
                sys.stderr.write("ERROR: Failed to parameterize lab container %s!\n" % container_name)
                sys.exit(1)
    
    # Reach here - Everything is OK - spawn terminal for each container based on num_terminal
    for (container_name, containerline) in containerslist.iteritems():
        #print containerline.container_dict()
        num_terminal = containerline.num_terminal
        #print "Number of terminal is %d" % num_terminal
        # If the number of terminal is zero -- do not spawn
        if num_terminal != 0:
            for x in range(0, num_terminal):
                spawn_command = "gnome-terminal -x docker exec -it %s bash -l &" % container_name
                os.system(spawn_command)

    return 0


# Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
def CreateHostHomeXfer(host_xfer_dir):
    # remove trailing '/'
    host_xfer_dir = host_xfer_dir.rstrip('/')
    #print "host_home_xfer directory (%s)" % host_xfer_dir
    if os.path.exists(host_xfer_dir):
        # exists but is not a directory
        if not os.path.isdir(host_xfer_dir):
            # remove file then create directory
            os.remove(host_xfer_dir)
            os.makedirs(host_xfer_dir)
        #else:
        #    print "host_home_xfer directory (%s) exists" % host_xfer_dir
    else:
        # does not exists, create directory
        os.makedirs(host_xfer_dir)

def ParseStartConfig(mycwd, labname):
    global container_name
    global container_image
    global container_user
    global host_home_xfer
    global lab_master_seed
    #print "ParseStartConfig for %s" % labname
    configfilename = '%s/start.config' % mycwd
    # Make sure start.config configuration file exists
    if not os.path.exists(configfilename):
        sys.stderr.write("Config file start.config does not exists!\n")
        sys.exit(1)
    configfile = open(configfilename)
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
                (key, value) = linestrip.split('=')
                key = key.strip()
                value = value.strip()
                # replace $lab with labname
                newvalue = value.replace('$lab', labname)
                # replace '"' with ''
                newvalue = newvalue.replace('"', '')
                #print "Key is (%s) with value (%s)" % (key, newvalue)
                if key == "CONTAINER_NAME":
                    container_name = newvalue
                    container_name_found = True
                elif key == "CONTAINER_IMAGE":
                    container_image = newvalue
                    container_image_found = True
                elif key == "CONTAINER_USER":
                    container_user = newvalue
                    container_user_found = True
                elif key == "HOST_HOME_XFER":
                    host_home_xfer = newvalue
                    host_home_xfer_found = True
                elif key == "LAB_MASTER_SEED":
                    lab_master_seed = newvalue
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

    return 0

# Usage: start.py <labname>
# Arguments:
#    <labname> - the lab to start
def main():
    #print "start.py -- main"
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: start.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    ParseStartConfig(mycwd, labname)
    #print "container_name is (%s)" % container_name
    #print "container_image is (%s)" % container_image
    #print "container_user is (%s)" % container_user
    #print "host_home_xfer is (%s)" % host_home_xfer
    #print "lab_master_seed is (%s)" % lab_master_seed

    # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
    host_xfer_dir = '%s/%s' % (myhomedir, host_home_xfer)
    CreateHostHomeXfer(host_xfer_dir)

    networkfilename = '%s/%s.network' % (mycwd, labname)
    # If <labname>.network exists, do multi-containers/multi-home networking
    # else do single container with default networking
    if not os.path.exists(networkfilename):
        DoSingle(mycwd, labname)
    else:
        DoMultiple(mycwd, labname)

    return 0

if __name__ == '__main__':
    sys.exit(main())

