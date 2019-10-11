#!/usr/bin/env python
import subprocess
import shlex
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
            retval[iface] = [ip, gw]

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

if __name__ == '__main__':
    if not checkContainers():
        routes = getRoutes()
        nets = getNets()
        for nid in nets:
            iface = 'br-%s' % nid
            if iface in routes:
                ip, gw = routes[iface]
                print('route %s %s for %s may be corrupting labtainers' % (ip, gw, iface))
                print('try running "docker network delete %s"' % iface)
