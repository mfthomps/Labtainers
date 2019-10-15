#!/usr/bin/env python
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
    for line in output[0].splitlines(True):
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
    for line in output[0].splitlines(True):
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
    for line in output[0].splitlines(True):
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
    for line in output[0].splitlines(True):
        if ip in line:
            retval = line
            break
    return retval

def checkLoop():
    retval = None
    cmd = 'sudo losetup -a'
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    for line in output[0].splitlines(True):
        if '/vfs/' in line:
            print('This loopback device may not have been cleaned up by Docker:\n%s' % line)
            dev = line.split(':',1)[0]
            print('Try removing with "sudo losetup -d %s' % dev)
      


if __name__ == '__main__':
    if not checkContainers():
        routes = getRoutes()
        nets = getNets()
        for nid in nets:
            iface = 'br-%s' % nid
            if iface in routes:
                ip, gw, mask = routes[iface]
                print('route %s %s for %s may be corrupting labtainers' % (ip, gw, iface))
                print('try running "docker network delete %s"' % iface)
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
           
        checkLoop()
    else:
        print('Containers are running, try stoplab.')
