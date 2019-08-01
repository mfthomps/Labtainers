#!/usr/bin/env python
import sys
import os
import argparse
import json
import shutil
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
Generate network files for GNS3 from a given Labtainers lab configuration.
The results go in the etc/network/interfaces file used by GNS3 startup.

This script also changes container names to match Labtainer conventions and will
copy a logo for use in the GNS3 workspace.
'''

def getLabtainerNodeId(gns3_json, name):
    for node in gns3_json['topology']['nodes']:
        #nn = node['name']
        if 'image' not in node['properties']:
            continue
        ni = node['properties']['image']
        if ni.startswith(name):
            print('matched node id %s' % node['node_id'])
            return node['node_id']
        if ni.startswith('mfthomps-'+name):
            print('matched node id %s' % node['node_id'])
            return node['node_id']
    return None

def setNodeName(gns3_json, node_id, name):
    for node in gns3_json['topology']['nodes']:
        if node['node_id'] == node_id:
            node['name'] = name
            return
    print('Failed to find node_id %s in json' % node_id)

home = os.getenv("HOME")
gns3_path = os.path.join(home, 'GNS3', 'projects')
labtainers_path = os.path.join(labtainer_dir, 'labs')
parser = argparse.ArgumentParser(description='Generate gns3 network interfaces file.')
parser.add_argument('labname', help='Name of labtainers lab')
parser.add_argument('gns3_proj', help='Name of gns3 project')
args = parser.parse_args()

print('labname: %s gns3: %s' % (args.labname, args.gns3_proj))
labutils.logger = LabtainerLogging.LabtainerLogging("genNet.log", 'eh', "../../config/labtainer.config")
gns3_proj = os.path.join(gns3_path, args.gns3_proj, args.gns3_proj+'.gns3')
if not os.path.isfile(gns3_proj):
    print('no gns3 proj file found at %s' % gns3_proj)
    exit(1)
labtainer_lab = os.path.join(labtainers_path, args.labname)
dumb, start_config = labutils.GetBothConfigs(labtainer_lab, labutils.logger)

with open(gns3_proj) as fh:
    gns3_json = json.load(fh)

'''
Look for logo
'''
logo_path = os.path.join(labtainer_lab, 'config', 'logo.png')
if os.path.isfile(logo_path):
    dest = os.path.join(gns3_path, args.gns3_proj, 'project-files', 'images')
    try:
        os.mkdir(dest)
    except:
        pass
    shutil.copy(logo_path, dest)
    about_path = os.path.join(labtainer_lab, 'config', 'about.txt')
    supplier = {}
    supplier['logo'] = 'logo.png'
    supplier['url'] = about_path
    gns3_json['supplier'] = supplier
   # print('logo path added! at %s' % logo_path)
else:
    print('no logo to copy at %s' % logo_path)

subnets = start_config.subnets

''' set node names and generate network interface files '''
for name, container in start_config.containers.items():
    print('container %s' % name)
    gns3_con = '%s_%s-labtainer' % (args.labname, name) 
    node_id = getLabtainerNodeId(gns3_json, gns3_con)
    if node_id is None:
       print('Could not find container %s in gns3 project json' % name)
       exit(1)
    setNodeName(gns3_json, node_id, name)
    iface_fname = os.path.join(gns3_path, args.gns3_proj, 'project-files', 'docker', node_id, 'etc','network','interfaces')
    with open(iface_fname, 'w') as fh:
        eth_index = 0
        for mysubnet_name, mysubnet_ip in container.container_nets.items():
            subnet_name = mysubnet_name
            print('subnet_name %s ip %s' % (mysubnet_name, mysubnet_ip))
            eth = 'eth%d' % eth_index
            netmask = IPNetwork(subnets[mysubnet_name].mask).netmask
            line = 'auto %s\niface %s inet static\n\taddress %s\n\tnetmask %s' % (eth, eth, mysubnet_ip, netmask)
            fh.write(line+'\n')
with open(gns3_proj, 'w') as fh:
    fh.write(json.dumps(gns3_json, indent=4))
    #json.dump(gns3_json, fh)



