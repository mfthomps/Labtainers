#!/usr/bin/env python
import os
import sys
import glob
import argparse

parser = argparse.ArgumentParser(description='Run a poll for a service')
parser.add_argument('service', help='name of the service')
parser.add_argument('num', help='poll number')
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
poll_dir = os.path.join('challenges', serve, 'polls')
plist = glob.glob(poll_dir+'/*.xml')
pnum = int(args.num)
if pnum > len(plist):
    print('Poll number out of range, max is %d' % len(plist))
    exit(1)
pname = 'GEN_00000_%05d.xml' % pnum
poll_path = os.path.join('challenges', serve, 'polls', pname)
cmd = '/usr/sbin/cb-replay --host %s --port %s  %s' % (ip, port, poll_path)
os.system(cmd)
