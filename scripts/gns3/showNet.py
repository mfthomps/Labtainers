#!/usr/bin/env python
import sys
import os
import argparse
import json
from netaddr import IPNetwork
labtainer_dir = os.getenv('LABTAINER_DIR')
if labtainer_dir is None:
    print('Must define LABTAINER_DIR environment variable')
    exit(1)
sys.path.append(os.path.join(labtainer_dir, 'scripts', 'labtainer-student','bin'))
sys.path.append(os.path.join(labtainer_dir, 'scripts', 'labtainer-student','lab_bin'))
import labutils
import LabtainerLogging
'''
Show network topology of a Labtainers lab
'''


labtainers_path = os.path.join(labtainer_dir, 'labs')
parser = argparse.ArgumentParser(description='Show Labtainer topology.')
parser.add_argument('labname', help='Name of labtainers lab')
args = parser.parse_args()

labutils.logger = LabtainerLogging.LabtainerLogging("showNet.log", 'eh', "../../config/labtainer.config")
labtainer_lab = os.path.join(labtainers_path, args.labname)
dumb, start_config = labutils.GetBothConfigs(labtainer_lab, labutils.logger)

nets = []
for subnet_name in start_config.subnets:
    #print('subnet: %s' % subnet_name)
    nets.append(subnet_name)

print('labname: %s has %d networks' % (args.labname, len(nets)))

for name, container in start_config.containers.items():
    eth_index = 0
    num_adapters = len(container.container_nets.items())
    print('Container: %s (# of adapters: %d)' % (name, num_adapters))
    for subnet_name, subnet_ip in container.container_nets.items():
        sub_index = nets.index(subnet_name)
        eth = 'eth %d' % eth_index
        print('\t %s to network %d' % (eth, sub_index))
        eth_index += 1




