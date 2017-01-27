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
    class Container():
        class ContainerNet():
            def __init__(self, ipaddr, gateway=None):
                self.ipaddr = ipaddr
                self.gateway = gateway
        def __init__(self, line):
            parts = line.split()
            self.term = 0
            self.container_name = parts[1].strip()
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
            name = parts[0][1:]
            ipaddr = parts[1].strip()
            try:
                IPNetwork(ipaddr)
            except:
                print('bad ip addr %s in \t%s' % (ipaddr, line))
                exit(1)
            gateway = None
            if len(parts) > 2:
                gateway = parts[2].strip()
                try:
                    IPNetwork(gateway)
                except:
                    print('bad ip addr %s in \t%s' % (gateway, line))
                    exit(1)
            self.container_nets[name] = self.ContainerNet(ipaddr, gateway)
        def toString(self):
            print('container: %s  image: %s  terms: %d' % (self.container_name, self.container_image,
                self.term))
            for subnet in self.container_nets:
                gw = ''
                if self.container_nets[subnet].gateway is not None:
                    gw = 'gateway:%s' % self.container_nets[subnet].gateway 
                print('\tsubnet: %s  ip: %s %s' % (subnet, self.container_nets[subnet].ipaddr, gw))
           
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

if __name__ == '__main__':
    multi_config = ParseMulti(sys.argv[1])
    for container in multi_config.containers:
        multi_config.containers[container].toString()
