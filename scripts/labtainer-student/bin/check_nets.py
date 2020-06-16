#!/usr/bin/env python
'''
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''
import subprocess
import shlex
'''
sudo iptables -t nat -v -L POSTROUTING -n --line-number
sudo iptables -t nat --delete POSTROUTING <line number>
sudo route del -net 192.168.1.0 netmask 255.255.255.0


/dev/loop16         0      0         0  0 /vfs/myfs.img                                        0     512

'''

def checkContainers():
    cmd = 'docker ps'
    retval = {}
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    retval = False
    for line in output[0].decode('utf-8').splitlines(True):
        if not line.startswith('CONTAINER'):
            parts = line.split()
            name = parts[-1]
            print('Container %s running, cannot run this diagnostic until all labs stopped' % name)
            print('Use stoplab, or docker stop to stop containers')
            retval = True
    return retval

def getRoutes():
    cmd = 'route -n'
    retval = {}
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    for line in output[0].decode('utf-8').splitlines(True):
        parts = line.split()
        if len(parts) == 8:
            iface = parts[7]
            ip = parts[0]
            gw = parts[1]
            mask = parts[2]
            retval[iface] = [ip, gw, mask]

    return retval

def getNets():
    cmd = 'docker network ls'
    retval = []
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    for line in output[0].decode('utf-8').splitlines(True):
        if not line.startswith('NETWORK'):
            parts = line.split()
            nid = parts[0]
            retval.append(nid)
    return retval

def getIPTable(ip):
    retval = None
    cmd = 'sudo iptables -t nat -v -L POSTROUTING -n --line-number'
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    for line in output[0].decode('utf-8').splitlines(True):
        if ip in line:
            retval = line
            break
    return retval

def checkLoop():
    retval = None
    cmd = 'sudo losetup -a'
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    for line in output[0].decode('utf-8').splitlines(True):
        if '/vfs/' in line:
            print('This loopback device may not have been cleaned up by Docker:\n%s' % line)
            dev = line.split(':',1)[0]
            print('Try removing with "sudo losetup -d %s"' % dev)

def checkNets():      
    retval = True
    if not checkContainers():
        routes = getRoutes()
        nets = getNets()
        for nid in nets:
            iface = 'br-%s' % nid
            if iface in routes:
                ip, gw, mask = routes[iface]
                print('route %s %s for %s may be corrupting labtainers' % (ip, gw, iface))
                print('try running "docker network delete %s"' % iface)
                retval = False
        for iface in routes:
            if iface.startswith('br-'):
                net_id = iface[3:]
                if net_id not in nets: 
                    ip, gw, mask = routes[iface]
                    print('route %s     %s     %s seems an orphan corrupting docker' % (ip, gw, mask))
                    print('try: sudo route del -net %s netmask %s' % (ip, mask))
                    iptable = getIPTable(ip)
                    if iptable is not None:
                        print('Also, this IPTABLE entry is maybe a problem: %s' % iptable)
                        num = iptable.split()[0]
                        print('Try: sudo iptables -t nat --delete POSTROUTING %s' % num)
                        retval = False
           
        checkLoop()
    else:
        print('Containers are running, try stoplab.')
    return retval


if __name__ == '__main__':
    checkNets()
