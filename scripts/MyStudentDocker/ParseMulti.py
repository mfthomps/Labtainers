#!/usr/bin/env python
import sys
from netaddr import *
import re
def isalphadashscore(name):
    # check name - alphanumeric,dash,underscore
    if re.match(r'^[a-zA-Z0-9_-]*$', name):
        return True
    else:
        return False
class ParseMulti():
    class Subnet():
        def __init__(self, line):
            parts = line.split()
            # Expecting 'NETWORK' format to be:
            # NETWORK <SUBNET_NAME> <SUBNET_NETWORK_MASK> [<SUBNET_GATEWAY>]
            if len(parts) != 3 and len(parts) != 4:
                print('Invalid SUBNET line (%s)' % line)
                exit(1)
            self.subnet_name = parts[1].strip()
            if not isalphadashscore(self.subnet_name):
                print('bad subnet name %s in \t%s' % (self.subnet_name, line))
                exit(1)
            self.subnet_mask = parts[2].strip()
            try:
                IPNetwork(self.subnet_mask)
            except:
                print('bad ip subnet %s in \t%s' % (self.subnet_mask, line))
                exit(1)
            if len(parts) == 4:
                self.subnet_gateway = parts[3].strip()
                if not IPAddress(self.subnet_gateway) in IPNetwork(self.subnet_mask):
                    print('Gateway IP (%s) not in subnet for SUBNET line(%s)!\n' % 
                           (self.subnet_gateway, self.subnet_mask))
                    exit(1)
            else:
                self.subnet_gateway = None
    class Container():
        class ContainerNet():
            def __init__(self, ipaddr):
                self.ipaddr = ipaddr
        def __init__(self, line):
            parts = line.split()
            self.term = 0
            self.container_name = parts[1].strip()
            # DO NOT allow '=' in container name
            if '=' in self.container_name:
                print('Character "=" is not allowed in container name (%s)' % parts[1].strip())
                exit(1)
            self.container_image = parts[2].strip()
            self.container_nets = {}
            if len(parts) > 3:
                try:
                    self.term = int(parts[3].strip())
                except:
                    print('Expected terminal count, got %s in \n%s' % (parts[3], line))
                    exit(1)
        def addNet(self, line):
            parts = line.split()
            # Expecting '+' (Container's SUBNET line) format to be:
            # +<SUBNET_NAME> <IP_ADDR>
            if len(parts) != 2:
                print("Invalid Container's SUBNET line (%s)" % line)
                exit(1)
            name = parts[0][1:]
            ipaddr = parts[1].strip()
            try:
                IPAddress(ipaddr)
            except:
                print('bad ip addr %s in \t%s' % (ipaddr, line))
                exit(1)
            self.container_nets[name] = self.ContainerNet(ipaddr)
        def toString(self):
            print('container: %s  image: %s  terms: %d' % (self.container_name, self.container_image,
                self.term))
            for subnet in self.container_nets:
                print('\tsubnet: %s  ip: %s' % (subnet, self.container_nets[subnet].ipaddr))
           
    def __init__(self, fname):
        self.subnets = {}
        self.containers = {}
        print('fname is %s' % fname)
        with open(fname) as fh:
            for line in fh:
                #print line
                if line.strip().startswith('NETWORK'):
                    if len(self.containers) > 0:
                        print('NETWORK found after container definition %s' % line)
                        exit(1)
                    new_subnet = self.Subnet(line)
                    if new_subnet.subnet_name not in self.subnets:            
                        self.subnets[new_subnet.subnet_name] = new_subnet
                    else:
                        print('duplicate subnet name %s in \t%s' % (new_subnet.subnet_name, line))
                        exit(1)
                elif line.strip().startswith('CONTAINER'):
                    new_container = self.Container(line)
                    if new_container.container_name not in self.containers:
                        self.containers[new_container.container_name] = new_container
                    else:
                        print('duplicate container name %s in \t%s' % (new_container.container_name, line))
                        exit(1)
                       
                elif line.strip().startswith('+'):
                    new_container.addNet(line)

        # Sanity checks
        # 1 - Each container must have at least one subnet
        # 2 - Each container's subnet must be a defined subnet
        # 3 - Each container's subnet IP address must be in the defined subnet IP range

if __name__ == '__main__':
    multi_config = ParseMulti(sys.argv[1])
    for container in multi_config.containers:
        multi_config.containers[container].toString()
