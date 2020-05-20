#!/usr/bin/env python
import os
import sys
import glob
import argparse

parser = argparse.ArgumentParser(description='Throw a pov at a service')
parser.add_argument('service', help='name of the service')
parser.add_argument('num', help='pov number')
parser.add_argument('-d', '--delay', action='store', default=0, help='Delay given seconds between connect and data exchange.  Intended to allow attaching a debug server to the service.')

args = parser.parse_args()

smap_file = 'service.map'
smap = {}
with open(smap_file) as fh:
    for line in fh:
        parts = line.split()
        smap[parts[0]] = parts[1].strip()

serve = args.service

if serve not in smap:
    print('service %s not found' % serve)
    exit(1)
ip = '172.25.0.3'
port = smap[serve]
poll_dir = os.path.join('challenges', serve, 'povs')
plist = glob.glob(poll_dir+'/*.pov')
pnum = int(args.num)
if pnum > len(plist):
    print('Poll number out of range, max is %d' % len(plist))
    exit(1)
pname = 'pov_%d.pov' % pnum
pov_path = os.path.join('challenges', serve, 'povs', pname)
cmd = './throw.py %s  %s %s' % (pov_path, port, args.delay)
os.system(cmd)
