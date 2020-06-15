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
import filecmp
import glob
import json
import hashlib
from hashlib import md5
import os
import shutil
import re
import subprocess
import sys
import time
import zipfile
import ParseStartConfig
import ParseLabtainerConfig
import datetime
import getpass
import socket
import fcntl
import struct
import threading
import LabCount
import shlex
import stat
import traceback
import string
import errno
import registry

''' assumes relative file positions '''
here = os.path.dirname(os.path.abspath(__file__))
lab_bin_dir = os.path.join(here, '../lab_bin')
sys.path.append(lab_bin_dir)
import ParameterParser
import InspectLocalReg
import InspectRemoteReg

''' logger is defined in whatever script that invokes the labutils '''
global logger

# Error code returned by docker inspect
SUCCESS=0
FAILURE=1

''' 
 Version number embeded as a label into each docker image.
 Current framework version (per below) must be at least
 what is found in the image.  This is only used for 
 framework/image compatibility, to tell a user that a given
 lab cannot be run without doing an update.
''' 
framework_version = 3

# Create a directory path based on input path
# Note: Do not create if the input path already exists as a directory
#       If input path is a file, remove the file then create directory
def createDirectoryPath(input_path):
    # if it exist as a directory, do not delete (only delete if it is a file)
    if os.path.exists(input_path):
        # exists but is not a directory
        if not os.path.isdir(input_path):
            # remove file then create directory
            os.remove(input_path)
            os.makedirs(input_path)
        #else:
        #    logger.debug("input_path directory (%s) exists" % input_path)
    else:
        # does not exists, create directory
        os.makedirs(input_path)

def isValidLab(lab_path):
    # Lab path must exist and must be a directory
    if os.path.exists(lab_path) and os.path.isdir(lab_path):
        # Assume it is valid lab then
        logger.debug("lab_path directory (%s) exists" % lab_path)
    else:
        logger.error("Invalid lab! lab_path directory (%s) does not exist!" % lab_path)
        #traceback.print_exc()
        #traceback.print_stack()
        sys.exit(1)


def getFirstUnassignedIface(n=1):
    ''' get the nth network iterface that lacks an assigned IP address '''
    iflist = os.listdir('/sys/class/net')
    for iface in sorted(iflist):
        count = 1
        ip = get_ip_address(iface)
        if ip is None and n == count:
            return iface
        count += 1
    return None

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sp = struct.pack('256s', str.encode(ifname[:15]))
    try:
        fc = fcntl.ioctl(s.fileno(), 0x8915, sp)
    except:
        return None
    return socket.inet_ntoa(fc[20:24])

def get_hw_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if sys.version_info >=(3,0):
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
        return ':'.join('%02x' % b for b in info[18:24])
    else:
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', str(ifname[:15])))
        return ':'.join(['%02x' % ord(char) for char in info[18:24]])

def get_new_mac(ifname):
    ''' use last two byte of mac address to generate a new mac
        intended for use on macvlan '''
    # TBD move this hardcoded prefix into some config file?
    preface = '02:43:ac:12'
    my_mac = get_hw_address(ifname)
    parts = my_mac.split(':')
    p1 = parts[4]
    p2 = parts[5]
    full = '%s:%s:%s' % (preface, p1, p2)
    return  full

def isalphadashscore(name):
    # check name - alphanumeric,dash,underscore
    return re.match(r'^[a-zA-Z0-9_-]*$', name)

# get docker0 IP address
def getDocker0IPAddr():
    #return get_ip_address('docker0')
    cmd = "docker inspect -f '{{ .NetworkSettings.IPAddress }}' docker0"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) == 0:
        ''' is a docker0 master container '''
        if len(output[0].strip()) > 0:
            return output[0].decode('utf-8').strip()
        else:
            return None
    else:
        return get_ip_address('docker0')

# Parameterize my_container_name container
def ParameterizeMyContainer(mycontainer_name, container_user, container_password, lab_instance_seed, 
                            user_email, labname, lab_path, name, image_info, running_container=None):
    retval = True
    if running_container == None:
        running_container = mycontainer_name
    ''' copy lab_bin and lab_sys files into .local/bin and / respectively '''
    CopyLabBin(running_container, container_user, lab_path, name, image_info)
    cmd_path = '/home/%s/.local/bin/parameterize.sh' % (container_user)
    if container_password == "":
        container_password = container_user

    version = '0'
    if image_info is None or image_info.version is None:
        ''' is a build, version -1 '''
        version = '-1'
    else:
        #print(str(image_info))
        if image_info.version is not None:
            version = image_info.version
    display = os.getenv('DISPLAY')
    command=['docker', 'exec', '-i',  running_container, cmd_path, container_user, container_password, lab_instance_seed, user_email, labname, mycontainer_name, version, display ]
    logger.debug("About to call parameterize.sh with : %s" % str(command))
    #return retval 
    child = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_string = child.stderr.read().decode('utf-8')
    if len(error_string) > 0:
        for line in error_string.splitlines(True):
            if  not line.startswith('[sudo]') and "LC_ALL" not in line and "ENCRYPT_METHOD" not in line:
                logger.error('ParameterizeMyContainer %s' % line)
                retval = False
            else:
                logger.debug(line)
    out_string = child.stdout.read().decode('utf-8').strip()
    if len(out_string) > 0:
        logger.debug('ParameterizeMyContainer %s' % out_string)
    return retval

def DoCmd(cmd):
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    retval = True
    if len(output[1]) > 0:
        logger.error(output[1].decode('utf-8'))
        retval = False
    if len(output[0]) > 0:
        logger.debug(output[0].decode('utf-8'))
    return retval

# Start my_container_name container
def StartMyContainer(mycontainer_name):
    retval = True
    if IsContainerRunning(mycontainer_name):
        logger.error("Container %s is already running!\n" % (mycontainer_name))
        sys.exit(1)
    command = "docker start %s" % mycontainer_name
    logger.debug("Command to execute is (%s)" % command)
    if not DoCmd(command):
        retval = False
    return retval

def AllContainersCreated(container):
    clone_names = GetContainerCloneNames(container)
    for clone_full in clone_names:
        if not IsContainerCreated(clone_full):
            return False
    return True

# Check to see if my_container_name container has been created or not
def IsContainerCreated(mycontainer_name):
    retval = True
    command = "docker inspect -f {{.Created}} --type container %s" % mycontainer_name
    logger.debug("Command to execute is (%s)" % command)
    result = subprocess.call(shlex.split(command), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if result == FAILURE:
       retval = False
    logger.debug("Result of subprocess.call for %s IsContainerCreated is %s (1=>FAILURE)" % (mycontainer_name, result))
    return retval

def GetNetParam(start_config, mysubnet_name, mysubnet_ip, mycontainer_name):
    ''' return the network address parameter and mac parameter for use in creating a container
        or connecting the container to a network.  Parse out mac address suffix if it exists,
        and adjust the ip address based on clone numbers if the address has a "+CLONE" suffix '''
    mac = ''
    ip_param = ''
    if ':' in mysubnet_ip:
        mysubnet_ip, mac_addr = mysubnet_ip.split(':',1)
        mac = '--mac-address=%s' % mac_addr 
    elif mysubnet_ip.lower() == 'auto_mac':
        mac_addr = get_new_mac(start_config.subnets[mysubnet_name].macvlan_use)
        mac = '--mac-address=%s' % mac_addr
    if not mysubnet_ip.lower().startswith('auto'):
        if '+' in mysubnet_ip:
            ip, clone_type = mysubnet_ip.split('+')
            if clone_type.lower() == 'clone' or start_config.multi_user == 'clones':
                name, role = mycontainer_name.rsplit('.',1)
                dumb, offset = name.rsplit('-', 1)
                try:
                    offset_int = int(offset) 
                except:
                    logger.error('expected use of clone, but did not find clone counter in %s' % mycontainer_name)
                    exit(1)
                ip_start, ip_suffix = ip.rsplit('.', 1)
                ip_suffix_int = int(ip_suffix)
                new_suffix = ip_suffix_int + offset_int - 1
                if new_suffix > 254:
                    logger.error('IP address adjusted to invalid value %d %s' % (new_suffix, mysubnet_ip))
                    exit(1)
                ip_param = '--ip=%s.%d' % (ip_start, new_suffix)
            elif clone_type.lower() == 'clone_mac' and start_config.multi_user == 'client':
                # assuming we are a multiuser client
                mac_addr = get_new_mac(start_config.subnets[mysubnet_name].macvlan_use)
                mac = '--mac-address=%s' % mac_addr

            else:
                print('ip %s' % ip)
                ip_param = '--ip=%s' % ip
                
        else:
            ip_param = '--ip=%s' % mysubnet_ip
    return ip_param, mac

def ConnectNetworkToContainer(start_config, mycontainer_name, mysubnet_name, mysubnet_ip):
    logger.debug("Connecting more network subnet to container %s" % mycontainer_name)
    ip_param, dumb = GetNetParam(start_config, mysubnet_name, mysubnet_ip, mycontainer_name)
    command = "docker network connect %s %s %s" % (ip_param, mysubnet_name, mycontainer_name)
    logger.debug("Command to execute is (%s)" % command)
    result = subprocess.call(shlex.split(command), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    logger.debug("Result of subprocess.call ConnectNetworkToContainer is %s" % result)
    return result

def DisconnectNetworkFromContainer(mycontainer_name, mysubnet_name):
    logger.debug("Disconnecting more network subnet to container %s" % mycontainer_name)
    command = "docker network disconnect %s %s" % (mysubnet_name, mycontainer_name)
    logger.debug("Command to execute is (%s)" % command)
    ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    result = 0
    if len(output[1]) > 0:
        logger.error(output[1].decode('utf-8'))
        result = 1;
    return result

def SetXhost():
    ''' allow container root users to access xserver '''
    cmd = 'xhost'
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if not 'LOCAL:' in output[0].decode('utf-8'):
        cmd = 'xhost local:root'
        os.system(cmd)
    
def GetContainerCloneNames(container):    
    ''' populate dictionary with hostname/container names based on the quantity of clones
        that are to be created '''
    retval = {}
    if container.clone_copies is None or container.clone == 1:
        retval[container.full_name] = container.hostname
    else:
        try:
            count = int(container.clone_copies)
        except:
            logger.error('bad clone value for %s' % container.hostname)
            exit(1)
        name, role = container.full_name.rsplit('.', 1)
        for i in range(1, count+1):
            hostname = '%s-%d' % (container.hostname, i)
            fullname = '%s-%d.%s' % (name, i, role)
            retval[fullname] = hostname
    return retval
       
def GetDNS_NMCLI(): 
    dns_param = ''
    dns_param = '--dns=8.8.8.8'
    cmd="nmcli dev show | grep 'IP4.DNS'"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0]) > 0: 
        for line in output[0].decode('utf-8').splitlines(True):
            dns_param = '--dns=%s %s' % (line.split()[1].strip(), dns_param)
            ''' just take first '''
            break
    return dns_param
def GetDNS(): 
    dns_param = ''
    dns_param = '--dns=8.8.8.8'
    cmd="systemd-resolve --status | grep 'DNS Servers:'"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0]) > 0: 
        for line in output[0].decode('utf-8').splitlines(True):
            dns_param = '--dns=%s %s' % (line.split()[2].strip(), dns_param)
            ''' just take first '''
            break
    else:
        dns_param = GetDNS_NMCLI()
    return dns_param

def GetX11SSH():
    ''' EXPERIMENTAL, not used '''
    ip = '192.168.1.222'
    xauth = '/tmp/.docker.xauth'
    #display = os.getenv('DISPLAY') 
    display = ':10'
    cmd = 'xauth list %s' % display
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0]) > 0: 
        parts = output[0].decode('utf-8').strip().split()
        magic_cookie = parts[2]
    else:
        print('could not find magic cookie')
        exit(1)
    x11_port = display.split(':')[1] 
    #print('x11_port %s' % x11_port)
    cmd = 'xauth -f /tmp/.docker.xauth add %s:%s . %s' % (ip, x11_port, magic_cookie)
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    os.chmod(xauth, 0o777)
    retval = '--env="%s:%s" -v %s:%s -e XAUTHORITY="%s"' % (ip, x11_port, xauth, xauth, xauth)
    #retval = '--env="DISPLAY" -v %s:%s -e XAUTHORITY="%s"' % (xauth, xauth, xauth)
    return retval 

def isUbuntuSystemd(image_name):
    done = False
    retval = False
    #print('check if %s is systemd' % image_name)
    cmd = "docker inspect -f '{{json .Config.Labels.base}}' --type image %s" % image_name
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].strip()) > 0:
            logger.debug('isUbuntuSystemd base %s' % output[0].decode('utf-8'))
            if output[0].decode('utf-8').strip() == 'null': 
                base = image_name
            else:
                base = output[0].decode('utf-8').rsplit('.', 1)[0]
                if base.startswith('"'):
                    base = base[1:]
                if '/' in base and '/' in image_name:
                    my_registry = image_name.split('/')[0]
                    no_reg = base.split('/')[1]
                    base = '%s/%s' % (my_registry, no_reg)
                
            cmd = "docker history --no-trunc %s" % base
            ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = ps.communicate()
            for line in output[0].decode('utf-8').splitlines():
                if 'Labtainer base image from ubuntu-systemd' in line:
                    retval = True
                    break

    return retval

def isFirefox(image_name):
    done = False
    retval = False
    #print('check if %s is systemd' % image_name)
    cmd = "docker inspect -f '{{json .Config.Labels.base}}' --type image %s" % image_name
    #print('lab container cmd is %s' % cmd)
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].strip()) > 0:
            logger.debug('base %s' % output[0].decode('utf-8'))
            if output[0].decode('utf-8').strip() == 'null': 
                base = image_name
            else:
                base = output[0].decode('utf-8').rsplit('.', 1)[0]+'"'
            cmd = "docker history --no-trunc %s" % base
            ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = ps.communicate()
            for line in output[0].decode('utf-8').splitlines():
                if 'firefox' in line:
                    retval = True
                    break

    return retval

def FindTapMonitor(start_config):
    for container_name in start_config.containers:
        #logger.debug('FindTapMonitor check %s' % container_name)
        for subnet in start_config.containers[container_name].container_nets:
            #logger.debug('FindTapMonitor check lan %s' % subnet)
            if subnet.lower() == 'tap_lan':
                ip = start_config.containers[container_name].container_nets[subnet]
                return container_name, ip
    return None, None

def HandleVolumes(volume, container):
    for m in container.mounts:
        logger.debug('adding volume mount %s' % m)
        ''' host volume is relative to ~/.local/share/labtainers, container relative to Home unless absolute '''
        try:
            hostv, containerv = m.split(':') 
        except:
            self.lgr.error('Bad mount definition %s' % m)
            exit(1)
        homedir = os.environ['HOME']
        host_path = os.path.join(homedir, '.local', 'share', 'labtainers', hostv)
        if not os.path.isfile(host_path):
            try:
                os.mkdir(host_path)
            except:
                pass
        container_path = os.path.join('/home', container.user, containerv) 
        volume = volume + ' -v %s:%s:rw' % (host_path, container_path)
    return volume

def CreateSingleContainer(labtainer_config, start_config, container, mysubnet_name=None, mysubnet_ip=None, quiet=False):
    ''' create a single container -- or all clones of that container per the start.config '''
    logger.debug("Create Single Container for %s" % container.name)
    retval = True
    #image_exists, result, new_image_name = ImageExists(container.image_name, container.registry)
    if container.registry == labtainer_config.test_registry:
        branch, container_registry = registry.getBranchRegistry()
        base_registry = container_registry
    else:
        container_registry = container.registry
        base_registry = container.base_registry
    image_info = imageInfo(container.image_name, container_registry, base_registry, labtainer_config, quiet=quiet)
    start_script = container.script     
    if image_info is None:
        logger.error('Could not find image for %s' % container.image_name)
        retval = False
    else:
        new_image_name = container.image_name
        if not image_info.local_build:
            new_image_name = '%s/%s' % (container_registry, container.image_name) 
        if not image_info.local:
            dockerPull(container_registry, container.image_name)
        docker0_IPAddr = getDocker0IPAddr()
        logger.debug("getDockerIPAddr result (%s)" % docker0_IPAddr)
        volume=''
        ubuntu_systemd = isUbuntuSystemd(new_image_name)
        is_firefox = isFirefox(new_image_name)
        if is_firefox:
            shm = '--shm-size=2g'
        else:
            shm = ''
        if container.script == '' or ubuntu_systemd:
            logger.debug('Container %s is systemd or has script empty <%s>' % (new_image_name, container.script))
            ''' a systemd container, centos or ubuntu? '''
            if ubuntu_systemd:
                ''' A one-off run to set some internal values.  This is NOT what runs the lab container '''
                start_script = ''
                #volume='--security-opt seccomp=confined --tmpfs /run --tmpfs /run/lock -v /sys/fs/cgroup:/sys/fs/cgroup:ro'
                volume='--security-opt seccomp=unconfined --tmpfs /run --tmpfs /run/lock -v /sys/fs/cgroup:/sys/fs/cgroup:ro'
                cmd = 'docker run --rm --privileged -v /:/host %s setup' % new_image_name
                logger.debug('cmd is %s' % cmd)
                ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                output = ps.communicate()
                logger.debug('back from docker run, output %s' % (output[0].decode('utf-8')))
                if len(output[1]) > 0:
                    logger.debug('back from docker run, error %s' % (output[1].decode('utf-8')))
                volume = '' 
            else:
                pass
                #volume='-v /sys/fs/cgroup:/sys/fs/cgroup:ro'
                #volume='--security-opt seccomp=unconfined --tmpfs /run --tmpfs /run/lock -v /sys/fs/cgroup:/sys/fs/cgroup:ro'
        if container.x11.lower() == 'yes':
            #volume = '-e DISPLAY -v /tmp/.Xll-unix:/tmp/.X11-unix --net=host -v$HOME/.Xauthority:/home/developer/.Xauthority'
            volume = volume+' --env="DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw"'
            logger.debug('container using X11')

        volume = HandleVolumes(volume, container)
        if container.mystuff.lower() == 'yes':
            here = os.getcwd()
            mystuff_dir = os.path.join(here, 'mystuff')
            myv = ' --volume="%s:/home/%s/mystuff:rw"' % (mystuff_dir, container.user)
            volume = volume+myv
            mystuff_dir = os.path.join(os.environ['LABTAINER_DIR'], 'scripts', 'labtainer-student','mystuff')
            try:
                os.mkdir(mystuff_dir)
            except:
                pass

        #if container.thumb_volume is not None:
        #    volume = volume+' --volume="/dev:/dev:rw"'
        #    #volume = volume+' --device="/dev/sdb"'

        add_hosts = ''     
        for item in container.add_hosts:
            if ':' not in item:
               if item in start_config.lan_hosts:
                   for entry in start_config.lan_hosts[item]:
                       add_this = '--add-host %s ' % entry
                       add_hosts += add_this
               else:
                   logger.error('ADD-HOST entry in start.config missing colon: %s' % item)
                   logger.error('sytax: ADD-HOST <host>:<ip>')
                   return
            else:
               add_this = '--add-host %s ' % item
               add_hosts += add_this
        if docker0_IPAddr is not None:
            add_host_param = '--add-host my_host:%s %s' % (docker0_IPAddr, add_hosts)
        else:
            add_host_param = ''
        if container.tap == 'yes':
            ''' docker fu when using host networking, sudo hangs looking for host ip? '''
            add_host_param = '--add-host %s:127.0.0.1 %s' % (container.hostname, add_host_param)
            monitor_tap, ip = FindTapMonitor(start_config)
            if monitor_tap is not None:
                add_host_param = '--add-host monitor_tap:%s %s' % (ip, add_host_param)
                wait_tap_dir = GetWaitTapDir()
                volume = '%s --volume %s:/tmp/wait_tap_dir' % (volume, wait_tap_dir)

            
        dns_param = GetDNS()
        priv_param = ''
        if container.no_privilege != 'yes':
            priv_param = '--privileged'
        publish_param = ''
        if container.publish is not None:
            publish_param = '--publish %s' % container.publish
        mac = ''
        subnet_ip = ''
        network_param = ''
        if container.tap == 'yes':
            network_param = '--network=host' 
            
        elif mysubnet_name is not None:
            network_param = '--network=%s' % mysubnet_name

        multi_user = ''
        if container.client == 'yes' and start_config.multi_user is not None:
            #print('use putenv to set %s' % start_config.multi_user)
            os.putenv("DISTRIBUTED_LABTAINER", start_config.multi_user)
            ''' why does putenv not set the value? '''
            os.environ['DISTRIBUTED_LABTAINER'] = start_config.multi_user
            multi_user = '--env=DISTRIBUTED_LABTAINER' 


        clone_names = GetContainerCloneNames(container)
        for clone_fullname in clone_names:
            clone_host = clone_names[clone_fullname]
            if mysubnet_name is not None:
                subnet_ip, mac = GetNetParam(start_config, mysubnet_name, mysubnet_ip, clone_fullname)
            #createsinglecommand = "docker create -t %s --ipc host --cap-add NET_ADMIN %s %s %s %s %s --name=%s --hostname %s %s %s %s %s" % (dns_param, 
            if len(container.docker_args) == 0:
                createsinglecommand = "docker create %s -t %s --cap-add NET_ADMIN %s %s %s %s %s %s --name=%s --hostname %s %s %s %s %s" % \
                    (shm, dns_param, network_param, subnet_ip, mac, priv_param, add_host_param,  
                    publish_param, clone_fullname, clone_host, volume, 
                    multi_user, new_image_name, start_script)
            else:
                createsinglecommand = "docker create %s %s --shm-size=2g -t %s --cap-add NET_ADMIN %s %s %s %s %s %s --name=%s --hostname %s %s %s %s %s" % \
                    (shm, container.docker_args, dns_param, network_param, subnet_ip, mac, priv_param, add_host_param,  
                    publish_param, clone_fullname, clone_host, volume, 
                    multi_user, new_image_name, start_script)
            logger.debug("Command to execute was (%s)" % createsinglecommand)
            ps = subprocess.Popen(shlex.split(createsinglecommand), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = ps.communicate()
            if len(output[1]) > 0:
                logger.debug('command was %s' % createsinglecommand)
                if 'Cannot connect to the Docker daemon' in output[1].decode('utf-8'):
                    print('\n\nERROR: Docker seems not to be running.')
                    print('Try "sudo systemctl restart docker"\n\n')
                logger.error('CreateSingleContainer %s' % output[1].decode('utf-8'))
                retval = False
                break
            #print('result of create %s' % output[0])

    return retval

def GetIface(ip):
    cmd = 'ifconfig | grep -B1 "inet addr:%s" | awk \'$1!="inet" && $1!="--" {print $1}\'' % ip
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    return output[0].decode('utf-8').strip()

def CheckPromisc(iface):
    cmd = "netstat -i | grep enp0s8 | awk '{print $12}'"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if 'P' in output[0].decode('utf-8'):
        return True
    else:
        return False

# Create SUBNETS
def CreateSubnets(start_config):
    has_tap = False
    subnets = start_config.subnets
    #for (subnet_name, subnet_network_mask) in networklist.iteritems():
    for subnet_name in subnets:
        subnet_network_mask = subnets[subnet_name].mask
        logger.debug("subnet_name is %s" % subnet_name)
        logger.debug("subnet_network_mask is %s" % subnet_network_mask)
        if subnets[subnet_name].tap:
            has_tap = True

        command = "docker network inspect %s" % subnet_name
        logger.debug("Command to execute is (%s)" % command)
        inspect_result = subprocess.call(shlex.split(command), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        logger.debug("Result of subprocess.call CreateSubnets docker network inspect is %s" % inspect_result)
        if inspect_result == FAILURE:
            # Fail means does not exist - then we can create
            macvlan = ''
            ip_range = ''
            net_type = 'bridge'
            if subnets[subnet_name].macvlan_use is not None:
                #iface = GetIface(subnets[subnet_name].macvlan)
                iface = subnets[subnet_name].macvlan_use
                if iface is None or len(iface) == 0:
                    logger.error("No IP assigned to network %s, assign an ip on Linux host to enable use of macvlan with Labtainers")
                    exit(1)
                if not CheckPromisc(iface):
                    logger.warning("network %s not in promisc mode, required for macvlan inter-vbox comms\nUse: sudo ifconfig %s promisc" % (iface, iface))
                macvlan = '-o parent=%s -o macvlan_mod=bridge' % iface
                net_type = 'macvlan'
            if subnets[subnet_name].ip_range is not None:
                ip_range = '--ip-range %s' % subnets[subnet_name].ip_range 
            if subnets[subnet_name].gateway != None:
                logger.debug(subnets[subnet_name].gateway)
                subnet_gateway = subnets[subnet_name].gateway
                command = "docker network create -d %s --gateway=%s --subnet %s %s %s %s" % (net_type, subnet_gateway, subnet_network_mask, macvlan, ip_range, subnet_name)
            else:
                command = "docker network create -d %s --subnet %s %s %s %s" % (net_type, subnet_network_mask, macvlan, ip_range, subnet_name)
            logger.debug("Command to execute is (%s)" % command)
            #create_result = subprocess.call(command, shell=True)
            ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = ps.communicate()
            logger.debug("stdout of subprocess.call CreateSubnets docker network create is %s" % output[0].decode('utf-8'))
            if len(output[1]) > 0:
                logger.debug('stderr of %s is %s' % (command, output[1].decode('utf-8')))
                found_match_network = False
                found_match_network_name = ""
                # Before a hard exit - give the user some indication of what to do next
                # First check to see if a gateway is provided and it is already used
                if 'no matching subnet' in output[1].decode('utf-8'):
                    logger.error('Config error: %s' % output[1].decode('utf-8'))
                    exit(1)
                if subnets[subnet_name].gateway != None:
                    found_match_network, found_match_network_name = FindNetworkGivenGatewayIP(subnets[subnet_name].gateway)
                    # If Gateway IP address not okay, no need to check subnet anymore
                    if not found_match_network:
                        # Gateway IP address might be okay but subnet mask might not
                        found_match_network, found_match_network_name = FindNetworkGivenSubnet(subnet_network_mask)
                else:
                    # No Gateway IP address, check the subnet mask only
                    found_match_network, found_match_network_name = FindNetworkGivenSubnet(subnet_network_mask)

                # At this point, if still not found then just print error and exit
                if not found_match_network:
                    logger.error("Failed to create %s subnet at %s, %s\n" % (subnet_name, subnet_network_mask, output[1].decode('utf-8')))
                    logger.error("command was %s\n" % command)
                    sys.exit(1)
                else:
                    # Found either a network matching the Gateway IP address or matching subnet
                    lablist = []
                    # See if any lab is using that network
                    lablist = GetListLabContainerOnNetwork(found_match_network_name)
                    if lablist == []:
                        # No lab is using the network - tell user to remove that "left-over" network
                        logger.error("An existing Docker network is preventing this lab from starting.")
                        logger.error("Try removing the network with:")
                        logger.error("docker network rm %s" % found_match_network_name)
                        sys.exit(1)
                    else:
                        # There is lab using that network - tell user to stop that lab first
                        logger.error("An existing Docker network is preventing this lab from starting.")
                        logger.error("This may be due to a failure to stop a previous lab.")
                        logger.error("Please stop the lab %s and try again." % lablist)
                        sys.exit(1)
        else:
            logger.warning("Already exists! Not creating %s subnet at %s!\n" % (subnet_name, subnet_network_mask))
    return has_tap
def RemoveSubnets(subnets, ignore_stop_error):
    for subnet_name in subnets:
        command = "docker network rm %s" % subnet_name
        logger.debug('command %s' % command)
        ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1].decode('utf-8')) > 0:
            if ignore_stop_error:
                logger.debug('Encountered error removing subnet %s' % subnet_name)
            else:
                logger.error('Encountered error removing subnet %s' % subnet_name)

EMAIL_TMP='./.tmp/email.txt' 
def getHomeEmail():
    ''' compatability for move of email to ~/.local/share/labtainers '''
    homedir = os.environ['HOME']
    lab_app = os.path.join(homedir,'.local', 'share', 'labtainers')
    logger.debug('getHomeEmail lab_app %s' % lab_app)
    try:
        os.makedirs(lab_app)
    except:
        pass
    email_path = os.path.join(lab_app, 'email.txt')
    if not os.path.isfile(email_path):
        logger.debug('getHomeEmail no email at %s' % email_path)
        if os.path.isfile(EMAIL_TMP):
            logger.debug('getHomeEmail copy from  %s' % EMAIL_TMP)
            shutil.copy(EMAIL_TMP, lab_app) 
        else:
            if 'LABTAINER_DIR' in os.environ:
                student_email = os.path.join(os.environ['LABTAINER_DIR'], 'scripts', 'labtainer-student','.tmp', 'email.txt')
                if os.path.isfile(student_email):
                    shutil.copy(student_email, lab_app) 
                else:
                    logger.debug('No email found at %s' % student_email)
            else:
                logger.debug('LABTAINER_DIR not in env, no email path found')
    return email_path


def getLastEmail():
    retval = None
    home_email = getHomeEmail()
    if os.path.isfile(home_email):
        with open(home_email) as fh:
            retval = fh.read()
            if retval is not None:
                retval = retval.strip()
    return retval

def putLastEmail(email):
    home_email = getHomeEmail()
    with open(home_email, 'w') as fh:
            fh.write(email)

def GetLabSeed(lab_master_seed, student_email):
    # Create hash using LAB_MASTER_SEED concatenated with user's e-mail
    # LAB_MASTER_SEED is per laboratory - specified in start.config
    string_to_be_hashed = '%s:%s' % (lab_master_seed, student_email)
    mymd5 = hashlib.new('md5')
    mymd5.update(string_to_be_hashed.encode('utf-8'))
    mymd5_hex_string = mymd5.hexdigest()
    return mymd5_hex_string

#def ParamStartConfig(lab_seed):
    
def ParamForStudent(lab_master_seed, mycontainer_name, container_user, container_password, labname, 
                    student_email, lab_path, name, image_info, running_container=None):
    if running_container == None:
        running_container = mycontainer_name

    mymd5_hex_string = GetLabSeed(lab_master_seed, student_email)
    logger.debug(mymd5_hex_string)

    if not ParameterizeMyContainer(mycontainer_name, container_user, container_password, mymd5_hex_string,
                                   student_email, labname, lab_path, name, image_info, running_container):
        logger.error("Failed to parameterize lab container %s!\n" % mycontainer_name)
        sys.exit(1)
    logger.debug('back from ParameterizeMyContainer for %s' % mycontainer_name)

def DockerCmd(cmd, noloop=False):
    ok = False
    count = 0
    if noloop:
        count = 1000
    while not ok:
        logger.debug("Command to execute is (%s)" % cmd)
        ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1].decode('utf-8')) > 0:
            count += 1
            logger.debug("Failed cmd %s %s" % (cmd, output[1].decode('utf-8')))
            if count > 1:
                return False
            time.sleep(1)
        else:
           ok = True
        if len(output[0].decode('utf-8')) > 0:
            logger.debug("cmd %s stdout: %s" % (cmd, output[0].decode('utf-8')))
            out = output[0].decode('utf-8')
            if 'unrecognized option' in out or 'Unexpected EOF' in out:
                return False
    return True


def CopyInstrConfig(mycontainer_name, container_user, lab_path):
    cmd = 'docker cp %s/instr_config/.  %s:/home/%s/.local/instr_config/' % (lab_path, mycontainer_name, container_user)
    if not DockerCmd(cmd):
        logger.error('failed %s' % cmd)
        exit(1)
    cmd = 'docker cp %s/config/.  %s:/home/%s/.local/config/' % (lab_path, mycontainer_name, container_user)
    if not DockerCmd(cmd):
        logger.error('failed %s' % cmd)
        exit(1)


def CopyLabBin(mycontainer_name, container_user, lab_path, name, image_info):
    here = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(here)
    lab_bin_path = os.path.join(parent, 'lab_bin')
    cmd = 'docker cp %s/.  %s:/home/%s/.local/bin/' % (lab_bin_path, mycontainer_name, container_user)
    if not DockerCmd(cmd):
        logger.error('failed %s' % cmd)
        exit(1)

    ''' TBD DO NOT move lab/config here -- would not catch the tar_list.txt files (skip list) '''
    ''' TBD perhaps move lab/_bin to here?  would it save duplicate containers?'''
    #container_bin = os.path.join(lab_path, name,'_bin')
    #if os.path.isdir(container_bin):
    #    cmd = 'docker cp %s/.  %s:/home/%s/.local/bin/' % (container_bin, mycontainer_name, container_user)
    #    DockerCmd(cmd)
    tmp_dir=os.path.join('/tmp/labtainers', mycontainer_name)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    try:
        os.makedirs(tmp_dir)
    except os.error:
        logger.error("did not expect to find dir %s" % tmp_dir)
    capinout = os.path.join(parent, 'lab_sys', 'sbin', 'capinout') 
    if not os.path.isfile(capinout):
        print('\n\n********* ERROR ***********')
        print('%s is missing.  If this is a development system, you may need to' % capinout)
        print('go to the tool-src/capinout directory and run ./mkit.sh')
        
    dest_tar = os.path.join(tmp_dir, 'labsys.tar')
    lab_sys_path = os.path.join(parent, 'lab_sys')

    cmd = 'tar cf %s -C %s sbin lib' % (dest_tar, lab_sys_path)
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) > 0:
        logger.error('tar failure %s result: %s' % (cmd, output[1].decode('utf-8')))

    cmd = 'docker cp %s %s:/var/tmp/' % (dest_tar, mycontainer_name)
    if not DockerCmd(cmd):
        logger.error('failed %s' % cmd)
        exit(1)

    cmd = 'docker exec %s script -q -c "sudo tar -x --keep-directory-symlink -f /var/tmp/labsys.tar -C /"' % (mycontainer_name)
    if not DockerCmd(cmd):
        '''
        cmd = 'docker exec %s script -q -c "sudo tar -x -f /var/tmp/labsys.tar -C /"' % (mycontainer_name)
        if not DockerCmd(cmd):
        '''
        cmd = 'docker cp lab_sys/.  %s:/' % (mycontainer_name)
        if not DockerCmd(cmd):
            logger.error('failed %s' % cmd)
            exit(1)
        logger.debug('CopyLabBin tar failed for lab_sys, explicit copy')

# Copy Students' Artifacts from host to instructor's lab container
def CopyStudentArtifacts(labtainer_config, mycontainer_name, labname, container_user, container_password):
    # Set the lab name 
    command = 'docker exec %s script -q -c "echo %s > /home/%s/.local/.labname" /dev/null' % (mycontainer_name, labname, container_user)
    logger.debug("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    logger.debug("Result of subprocess.call CopyStudentArtifacts set labname is %s (1=>FAILURE)" % result)
    if result == FAILURE:
        logger.error("Failed to set labname in container %s!\n" % mycontainer_name)
        sys.exit(1)

    # Create is_grade_container
    command = 'docker exec %s script -q -c "echo TRUE > /home/%s/.local/.is_grade_container" /dev/null' % (mycontainer_name, container_user)
    logger.debug("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    logger.debug("Result of subprocess.call CopyStudentArtifacts create is_grade_container is %s (1=>FAILURE)" % result)
    if result == FAILURE:
        logger.error("Failed to create is_grade_container in container %s!\n" % mycontainer_name)
        sys.exit(1)

    username = getpass.getuser()
    xfer_dir = os.path.join(labtainer_config.host_home_xfer, labname)
    zip_filelist = glob.glob('/home/%s/%s/*.zip' % (username, xfer_dir))
    logger.debug("filenames is (%s)" % zip_filelist)
    # Copy zip files from 'Shared' folder to 'home/$CONTAINER_USER'
    for fname in zip_filelist:
        logger.debug("name is %s" % fname)
        base_fname = os.path.basename(fname)
        # Copy zip file 
        command = 'docker cp %s %s:/home/%s/' % (fname, mycontainer_name, container_user)
        logger.debug("Command to execute is (%s)" % command)
        result = subprocess.call(shlex.split(command))
        logger.debug("Result of subprocess.call CopyStudentArtifacts copy zipfile (%s) is %s (1=>FAILURE)" % (fname, result))
        if result == FAILURE:
            logger.error("Failed to copy student artifacts into container %s!\n" % mycontainer_name)
            sys.exit(1)
        #command = 'docker exec %s echo "%s\n" | sudo -S chown %s:%s /home/%s/%s' % (mycontainer_name, container_password, 
        #             container_user, container_user, container_user, base_fname)
        #command = 'docker exec %s chown %s:%s /home/%s/%s' % (mycontainer_name, 
        #             container_user, container_user, container_user, base_fname)
        #logger.debug("Command to execute is (%s)" % command)
        #result = subprocess.call(command, shell=True)
        #logger.debug("Result of subprocess.call CopyStudentArtifacts copy zipfile (%s) is %s" % (fname, result))
        #if result == FAILURE:
        #    logger.error("Failed to set labname in container %s!\n" % mycontainer_name)
        #    sys.exit(1)

def GetRunningContainersList():
    cmd = "docker container ls --format {{.Names}}"
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].decode('utf-8').strip()) > 0:
        logger.debug('No running containers: error returned %s, return false' % output[1].decode('utf-8'))
        return False, None
    result = output[0].decode('utf-8').strip()
    logger.debug('result is %s' % result)
    if 'Error:' in result or len(result.strip()) == 0:
        if 'Error:' in result:
            logger.debug("Command was (%s)" % cmd)
            logger.debug("Error from command = '%s'" % result)
        return False, result
    containers_list = result.split('\n')
    return True, containers_list

def GetRunningLabNames(containers_list):
    labnameslist = []
    found_lab_role = False
    for each_container in containers_list:
        #print each_container
        if each_container.endswith('.student'):
            splitstring = each_container.split('.')
            labname = splitstring[0]
            found_lab_role = True
            if labname not in labnameslist:
                labnameslist.append(labname)
    return found_lab_role, labnameslist

class ImageInfo():
    def __init__(self, name, creation, user, local, local_build, version, use_tag):
        self.name = name
        self.creation = creation
        self.user = user
        self.local = local
        ''' whether a locally built image '''
        self.local_build = local_build  
        self.version =  None
        self.use_tag = use_tag
        if version is not None:
            version = version.replace('"', '')
            if version != 'null' and len(version.strip()) > 0:
                try:
                    self.version = version
                except:
                    logger.error('failed getting version from string <%s>' % version)
                    traceback.print_exc()
                    traceback.print_stack()
                    exit(1)

def inspectImage(image_name):
    created = None
    user = None
    version = None
    cmd = "docker inspect -f '{{.Created}}' --type image %s" % image_name
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].decode('utf-8').strip()) > 0:
        created = output[0].decode('utf-8').strip()
    cmd = "docker inspect -f '{{.Config.User}}' --type image %s" % image_name
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].decode('utf-8').strip()) > 0:
        user = output[0].decode('utf-8').strip()
    cmd = "docker inspect --format='{{json .Config.Labels.version}}' --type image %s" % image_name
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].decode('utf-8').strip()) > 0:
        version = output[0].decode('utf-8').strip()
    return created, user, version

def imageInfo(image_name, registry, base_registry, labtainer_config, is_rebuild=False, no_pull=False, quiet=False, local_build=False):
    ''' image_name lacks registry info (always) 
        First look if plain image name exists, suggesting
        an ongoing build/test situation '''    
    retval = None
    use_tag = 'latest'
    created, user, version = inspectImage(image_name)
    if created is not None:
        retval = ImageInfo(image_name, created, user, True, True, version, use_tag) 
        logger.debug('%s local built, ts %s %s' % (image_name, created, user)) 
    else:
        ''' next see if there is a local image from the desired registry '''
        with_registry = '%s/%s' % (registry, image_name)
        created, user, version = inspectImage(with_registry)
        if created is not None:
            retval = ImageInfo(with_registry, created, user, True, False, version, use_tag) 
            logger.debug('%s local from reg, ts %s %s version: %s' % (with_registry, created, user, version)) 
        elif not local_build:
            ''' See if the image exists in the desired registry '''
            reg_host = None
            if ':' in labtainer_config.test_registry:
                reg_host = labtainer_config.test_registry.split(':')[0]
            if reg_host is not None and registry.startswith(reg_host):
                created, user, version, use_tag, base = InspectLocalReg.inspectLocal(image_name, logger, 
                                  registry, is_rebuild=is_rebuild, quiet=quiet, no_pull=no_pull)
            else:
                created, user, version, use_tag = InspectRemoteReg.inspectRemote(with_registry, logger, 
                                  is_rebuild=is_rebuild, quiet=quiet, no_pull=no_pull, base_registry=base_registry)
                if created is None and not is_rebuild:
                    if not InspectRemoteReg.reachDockerHub():
                        logger.error('Unable to reach DockerHub.  \nIs the network functional?\n')
            if created is not None:
                logger.debug('%s only on registry %s, ts %s %s version %s use_tag %s' % (with_registry, registry, created, user, version, use_tag)) 
                retval = ImageInfo(with_registry, created, user, False, False, version, use_tag)
    if retval is None:
        logger.debug('%s not found local_build was %r' % (image_name, local_build))

    return retval

def GetBothConfigs(lab_path, logger, servers=None, clone_count=None):
    labtainer_config_dir = os.path.join(os.path.dirname(os.path.dirname(lab_path)), 'config', 'labtainer.config')
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config_dir, logger)
    labname = os.path.basename(lab_path)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, 
                       labtainer_config, logger, servers=servers, clone_count=clone_count)
    return labtainer_config, start_config

def dockerPull(registry, image_name):
    cmd = 'docker pull %s/%s' % (registry, image_name)
    logger.debug('%s' % cmd)
    print('pulling %s from %s' % (image_name, registry))
    ps = subprocess.Popen(shlex.split(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1]) > 0:
        return False
    print('Done with pull')
    return True


def defineAdditionalIP(container_name, post_start_if, post_start_nets):
    for subnet in post_start_nets:
        existing_ip = post_start_if[subnet]
        cmd = "docker exec %s bash -c 'ifconfig'" % (container_name)
        logger.debug('cmd is %s' % cmd)
        ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        logger.debug('out0 %s \nout1 %s' % (output[0].decode('utf-8'), output[1].decode('utf-8')))
        current_if = None
        this_if = None
        for line in output[0].decode('utf-8').splitlines():
            parts = line.split()
            if len(parts) < 2:
                continue
            if parts[1] == 'Link':
                current_if = parts[0]
            elif parts[1] == ('addr:%s' % post_start_if[subnet]):
                this_if = current_if
                break
        count = 1
        for ip in post_start_nets[subnet]:
            cmd = "docker exec %s bash -c 'ifconfig %s:%d %s'" % (container_name, this_if, count, ip)
            logger.debug('next cmd is %s' % cmd)
            if not DockerCmd(cmd):
                print('error doing %s' % cmd)
                exit(1) 
            count += 1
    
def MakeNetMap(start_config, mycontainer_name, container_user): 
    ''' filter docker network list to include only tapped lans, and append MAC to each line '''
    cmd = "docker network ls"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    nlist = []
    for subnet in start_config.subnets:
        if start_config.subnets[subnet].tap == 'yes':
            nlist.append(subnet)
    if len(output[1].strip()) == 0:
        with open('/tmp/net_map.txt', 'w') as fh:
            ''' for each network reported by docker '''
            for line in output[0].decode('utf-8').splitlines():
                parts = line.split()
                net = parts[1]
                eth = 'br-%s' % parts[0]
                ''' find if it matches a tapped subnet in this lab '''
                for subnet in nlist:
                    if subnet == net:
                        mac = get_hw_address(eth)
                        new_line = '%s %s\n' % (line, mac)
                        fh.write(new_line)
                        break
        cmd = 'docker cp /tmp/net_map.txt  %s:/var/tmp/' % (mycontainer_name)
        DockerCmd(cmd)
       
def WaitForTap():
    tap_dir = GetWaitTapDir()
    tap_lock = os.path.join(tap_dir,'lock')
    while not os.path.isdir(tap_lock):
        logger.debug('tap dir does not yet exist')
        time.sleep(1)
    
def DoStartOne(labname, name, container, start_config, labtainer_config, lab_path,  
               student_email, quiet_start, results, auto_grade, image_info):
        retval = True
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        container_user         = container.user
        container_password         = container.password
        container_hostname         = container.hostname
        ''' mananage interfaces with multiple IP addresses, docker does not support directly '''
        post_start_if = {}
        post_start_nets = {}

        haveContainer = AllContainersCreated(container)
        logger.debug("DoStart for %s AllContainersCreated result (%s)" % (container.name, haveContainer))

        # Set need_seeds=False first
        need_seeds=False
        # IsContainerCreated return False if container does not exists
        if not haveContainer:
            # Container does not exist, create the container
            # Use CreateSingleContainer()
            containerCreated = False
            if len(container.container_nets) == 0 or container.tap == 'yes':
                containerCreated = CreateSingleContainer(labtainer_config, start_config, container, quiet=quiet_start)
            else:
                #mysubnet_name, mysubnet_ip = container.container_nets.popitem()
                mysubnet_name = next(iter(container.container_nets))
                mysubnet_ip = container.container_nets[mysubnet_name]
                container.did_net(mysubnet_name)
                subnet_name = mysubnet_name
                if ':' in mysubnet_name:
                    subnet_name = mysubnet_name.split(':')[0] 
                    post_start_if[subnet_name] = mysubnet_ip
                containerCreated = CreateSingleContainer(labtainer_config, start_config, container, subnet_name, mysubnet_ip, quiet=quiet_start)
                
            logger.debug("CreateSingleContainer %s result (%s)" % (mycontainer_name, containerCreated))
            if not containerCreated:
                logger.error("CreateSingleContainer fails to create container %s!\n" % mycontainer_name)
                results.append(False)
                return

            # Give the container some time -- just in case
            #time.sleep(3)
            # If we just create it, then set need_seeds=True
            need_seeds=True

        # Check again - 
        haveContainer = AllContainersCreated(container)
        logger.debug("AllContainersCreated second check for %s result (%s)" % (container.name, haveContainer))

        # IsContainerCreated returned False if container does not exists
        if not haveContainer:
            logger.error("Container %s still not created!\n" % mycontainer_name)
            results.append(False)
            return
       
        clone_names = GetContainerCloneNames(container)
        for mycontainer_name in clone_names:
            wait_for_tap = False
            for mysubnet_name, mysubnet_ip in container.container_nets.items():
                if start_config.subnets[mysubnet_name].tap:
                    wait_for_tap = True
                if mysubnet_name in container.did_nets:
                    continue
                
                subnet_name = mysubnet_name
                if ':' in mysubnet_name:
                    subnet_name = mysubnet_name.split(':')[0] 
                    if subnet_name not in post_start_nets:
                        post_start_nets[subnet_name] = []
                    if subnet_name not in post_start_if:
                        post_start_if[subnet_name] = mysubnet_ip
                        logger.debug('container: %s assigned post_start_if[%s] %s, connecting' % (mycontainer_name, subnet_name, mysubnet_ip))
                        connectNetworkResult = ConnectNetworkToContainer(start_config, mycontainer_name, subnet_name, mysubnet_ip)
                    else:
                        post_start_nets[subnet_name].append(mysubnet_ip)
                else:
                    connectNetworkResult = ConnectNetworkToContainer(start_config, mycontainer_name, mysubnet_name, mysubnet_ip)
            if wait_for_tap:
                WaitForTap()
            # Start the container
            if not StartMyContainer(mycontainer_name):
                logger.error("Container %s failed to start!\n" % mycontainer_name)
                results.append(False)
                return
            defineAdditionalIP(mycontainer_name, post_start_if, post_start_nets)

            clone_need_seeds = need_seeds
            if not clone_need_seeds:
                cmd = "docker exec %s bash -c 'ls -l /var/labtainer/did_param'" % (mycontainer_name)
                if not DockerCmd(cmd):
                   print('One or more containers exists but are not parameterized.')
                   print('Please restart this lab with the "-r" option.')
                   DoStop(start_config, labtainer_config, lab_path, False)
                   logger.error('One or more containers exists but not parameterized.')
                   sys.exit(1)
    
            # If the container is just created, then use the previous user's e-mail
            # then parameterize the container
            elif quiet_start and clone_need_seeds:
                ParamForStudent(start_config.lab_master_seed, mycontainer_name, container_user, container_password, 
                                labname, student_email, lab_path, name, image_info)
            
            elif clone_need_seeds:
                ParamForStudent(start_config.lab_master_seed, mycontainer_name, container_user, 
                                                 container_password, labname, student_email, lab_path, name, image_info)
            if container.no_gw:
                cmd = "docker exec %s bash -c 'sudo /bin/ip route del 0/0'" % (mycontainer_name)
                DockerCmd(cmd)
                cmd = "docker exec %s bash -c 'sudo route del default'" % (mycontainer_name)
                DockerCmd(cmd)
            if container.tap == 'yes':
                MakeNetMap(start_config, mycontainer_name, container_user)
            if container.lab_gateway is not None:
                cmd = "docker exec %s bash -c 'sudo /usr/bin/set_default_gw.sh %s'" % (mycontainer_name, 
                        container.lab_gateway)
                if not DockerCmd(cmd):
                    logger.error('Fatal error in docker command %s' % cmd) 
                    results.append(False)
                    return
                cmd = "docker exec %s bash -c 'sudo echo \"nameserver %s\" >/etc/resolv.conf'" % (mycontainer_name, 
                        container.lab_gateway)
                if not DockerCmd(cmd):
                    logger.error('Fatal error in docker command %s' % cmd) 
                    results.append(False)
                    return
                cmd = "docker exec %s bash -c 'sudo route del my_host'" % (mycontainer_name)
                DockerCmd(cmd)
    
        results.append(retval)

def GetUserEmail(quiet_start):
    user_email = None
    while user_email is None:
        done = True
        # Prompt user for e-mail address
        eprompt = 'Please enter your e-mail address: '
        prev_email = getLastEmail()
        if prev_email is not None:
            eprompt = eprompt+" [%s]" % prev_email

             #checks if quiet_start is true
        if quiet_start and prev_email is not None:
            user_email = prev_email
        else:
            if sys.version_info >=(3,0):
                user_input = input(eprompt)
            else:
                user_input = raw_input(eprompt)
            if not all(c in string.printable for c in user_input):
                print('Bad characters detected.  Please re-enter email')
            else:
                user_email = user_input 
        if user_email is not None:
            #user_email = input(eprompt)
            if len(user_email.strip()) == 0:
                if prev_email is None:
                    print('You have provided an empty email address, which may cause your results to not be graded.')
                    if sys.version_info >=(3,0):
                        confirm = str(input('Use the empty address? (y/n)')).lower().strip()
                    else:
                        confirm = str(raw_input('Use the empty address? (y/n)')).lower().strip()
                    if confirm != 'y':
                        user_email = None
                else:
                    user_email = prev_email
            else:
                putLastEmail(user_email)
    return user_email

def CheckLabContainerApps(start_config, lab_path, apps2start):
    apps2search = ['firefox', 'wireshark']
    has_multi_container = False
    num_containers = len(start_config.containers.items())
    if num_containers > 1:
        has_multi_container = True

    apps2startfilepath = os.path.join(lab_path, '*/_bin', 'student_startup.sh')
    apps2start_list = glob.glob('%s' % apps2startfilepath)

    if apps2start_list != []:
        # Parse each student_startup.sh - get a list of apps to start
        # Currently only search for firefox or wireshark
        for eachfile in apps2start_list:
            with open(eachfile) as fh:
                for line in fh:
                    if line.startswith('#') or len(line) == 0:
                        continue
                    for apps in apps2search:
                        if apps in line:
                            if apps not in apps2start:
                                apps2start.append(apps)

    return has_multi_container

def ReloadStartConfig(lab_path, labtainer_config, start_config, student_email, logger, servers, clone_count):

    labname = os.path.basename(lab_path)
    my_start_config = os.path.join('./.tmp',labname, 'start.config')
    if not os.path.isfile(my_start_config):
        config_path       = os.path.join(lab_path,"config") 
        start_config_path = os.path.join(config_path,"start.config")
        param_path = os.path.join(config_path,"parameter.config")
        try:
            os.makedirs(os.path.dirname(my_start_config))
        except os.error:
            pass
        shutil.copyfile(start_config_path, my_start_config)
        lab_instance_seed = GetLabSeed(start_config.lab_master_seed, student_email)
        logger.debug("lab_instance_seed for <%s> <%s> is %s" % (start_config.lab_master_seed, student_email, lab_instance_seed))
        pp = ParameterParser.ParameterParser(None, None, lab_instance_seed, logger, lab=labname)
        pp.ParseParameterConfig(param_path)
        pp.DoReplace()
    start_config = ParseStartConfig.ParseStartConfig(my_start_config, labname, labtainer_config, logger, skip_networks=False,
                         servers=servers, clone_count=clone_count)
    logger.debug('did start.config reload from %s' % my_start_config)
    return start_config


def CheckEmailReloadStartConfig(start_config, quiet_start, lab_path, labtainer_config, logger, servers, clone_count):
    student_email = None
    for name, container in start_config.containers.items():
        # Obscure means of making sure we have an email and getting one if
        # a container has not yet been created.
        if not AllContainersCreated(container) and student_email is None:
            if student_email == None:
                student_email = GetUserEmail(quiet_start)
            else:
                student_email = GetUserEmail(True)
    if student_email == None:
        student_email = GetUserEmail(True)
    start_config = ReloadStartConfig(lab_path, labtainer_config, start_config, student_email, logger, servers, clone_count)
    return start_config, student_email

def pidExists(pid):
    """Check whether pid exists in the current process table.
    UNIX only.
    """
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH)
            raise
    else:
        return True

def ContainerTerminals(lab_path, start_config, container, terminal_count, terminal_groups, container_map):
    num_terminal = int(container.terminals)
    clone_names = GetContainerCloneNames(container)
    for mycontainer_name in clone_names:
        logger.debug("container: %s  Number of terminals: %d" % (mycontainer_name, num_terminal))
        if mycontainer_name in container_map:
            logger.debug('container %s mapped to %s' % (mycontainer_name, container_map[mycontainer_name]))
            mycontainer_name = container_map[mycontainer_name]
        CopyFilesToHost(lab_path, container.name, mycontainer_name, container.user)
        ''' HACK remove after a while....  catch case where framework updated to remove XTERM Instructions, but still using image
            that includes instructions, which then consumes a window '''
        if container.xterm is None:
            cmd = "docker exec %s bash -c 'ls -l $HOME/instructions.txt'" % (mycontainer_name)
            if DockerCmd(cmd, noloop=True):
                logger.debug('Found instructions, force xterm')
                container.xterm = 'instructions'

        if container.xterm is not None:
                logger.debug('container.xterm is <%s>' % container.xterm)
                parts = container.xterm.split()
                title = parts[0]
                command = None
                if title.lower() == 'instructions' and len(parts) == 1:
                    command = 'startup.sh'
                elif len(parts) == 2:
                    command = parts[1]
                else:
                    logger.error("Bad XTERM entryin in start.config: %s" % container.xterm)
                    exit(1)
                if command is not None:
                    cmd =  'sh -c "cd /home/%s && .local/bin/%s"' % (container.user, command)
                    terminal_location, columns, lines = terminalCounter(terminal_count)
                    terminal_count += 1
                    # note hack to change --geometry to -geometry
                    spawn_command = "xterm %s -title %s -sb -rightbar -fa 'Monospace' -fs 11 -e docker exec -it %s %s  & 2>/tmp/xterm.out" % (terminal_location[1:], 
                         title, mycontainer_name, cmd)
                    logger.debug("xterm spawn: %s" % spawn_command)
                    xterm_pid = subprocess.Popen(shlex.split(spawn_command), stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True).pid
                    # race condition, gnome may beat xterm to the startup.sh script
                    if command == 'startup.sh':
                        done = False
                        while pidExists(xterm_pid) and not done:
                            cmd = 'docker exec -it %s ls -l /tmp/.mylockdir' % mycontainer_name
                            ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                            output = ps.communicate()
                            if 'No such file or directory' not in output[0].decode('utf-8'):
                                done = True
                            else:
                                time.sleep(0.2)
                    
        # If the number of terminals is -1 or zero -- do not spawn
        if not (num_terminal == 0 or num_terminal == -1):
            for x in range(num_terminal):
                #sys.stderr.write("%d \n" % terminal_count)
                terminal_location, columns, lines = terminalCounter(terminal_count)
                #sys.stderr.write("%s \n" % terminal_location)
                #sys.stderr.write("%s \n" % mycontainer_name)
                cmd = 'bash -l' 
                #spawn_command = "gnome-terminal %s -x docker exec -it %s bash -l &" % (terminal_location, mycontainer_name)
                if container.terminal_group is not None:
                    if container.terminal_group not in terminal_groups:
                        terminal_count += 1
                        terminal_groups[container.terminal_group] = []
                    group_command = '"docker exec -it %s %s"' % (mycontainer_name, cmd)
                    terminal_groups[container.terminal_group].append(group_command)
                else:
                    terminal_count += 1
                    spawn_command = 'gnome-terminal %s -- docker exec -it --env COLUMNS=%d --env LINES=%d %s %s &' % (terminal_location,
                       columns, lines, mycontainer_name, cmd)
                    logger.debug("gnome spawn: %s" % spawn_command)
                    #print spawn_command
                    os.system(spawn_command)
    return terminal_count

def SkipContainer(run_container, name, start_config, servers):
    container = start_config.containers[name]
    if run_container is not None and container.full_name != run_container:
        return True
    if servers is not None:
        if servers == 'server':
            if container.client == 'yes':
                return True
        elif servers == 'client':
            if container.client != 'yes':
                return True
    return False

def readFirst(lab_path, labname, fname, quiet_start, bail_option=False):
    #
    #  If a fname exists in the lab's config directory, less it before the student continues.
    #
    doc_dir = os.path.join(lab_path, 'docs')
    read_first = os.path.join(doc_dir, fname)
    pdf = '%s.pdf' % labname
    manual = os.path.join(doc_dir, pdf)

    if os.path.isfile(read_first):
        print('\n\n')
        command = 'cat %s' % read_first
        less = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        sed_cmd = "sed -e s+LAB_MANUAL+%s+ -e s+LAB_DOCS+%s+" %  (manual, doc_dir)
        sed = subprocess.Popen(sed_cmd.split(), stdin=less.stdout, stdout=subprocess.PIPE)
        output = sed.communicate()[0].decode('utf-8')
        print(output)
        if not quiet_start: 
            less.wait()
            if not bail_option:
                if sys.version_info >=(3,0):
                    dumb = input("Press <enter> to start the lab\n")
                else:
                    dumb = raw_input("Press <enter> to start the lab\n")
            else:
                if sys.version_info >=(3,0):
                    dumb = input("Continue? (y/n)")
                else:
                    dumb = raw_input("Continue? (y/n)")
                if dumb.lower() != 'y':
                    cmd = 'rm -fr .tmp/%s' % labname
                    os.system(cmd)
                    print('Exiting lab')
                    exit(0)

def DoTerminals(start_config, lab_path, run_container=None, servers=None, container_map={}):
    # spawn terminal for each container based on num_terminal
    terminal_count = 0
    terminal_groups = {}
    for name, container in start_config.containers.items():
        # Do not spawn terminal if it is regression testing
        if SkipContainer(run_container, name, start_config, servers):
            print('herez %s' % name)
            continue
        terminal_count = ContainerTerminals(lab_path, start_config, container, terminal_count, terminal_groups, container_map)

    for tg in terminal_groups:
        tab_commands = ''
        tab = '--window'
        for command in terminal_groups[tg]:
            tab_commands = tab_commands+' %s -e %s' % (tab, command)
            tab = '--tab'
            #tab_commands = tab_commands+' --tab %s --' % command
        terminal_location, columns, lines = terminalCounter(terminal_count)
        terminal_count += 1
        spawn_command = 'gnome-terminal %s %s' % (terminal_location, tab_commands)
        FNULL = open(os.devnull, 'w')
        result = subprocess.Popen(shlex.split(spawn_command), close_fds=True, stdout=FNULL, stderr=subprocess.STDOUT)
        logger.debug("gnome spawn: %s" % spawn_command)
        #os.system(spawn_command)

def GetWaitTapDir():
    user = os.getenv('USER')
    wait_tap_dir = os.path.join('/tmp', user, 'wait_tap_dir')
    return wait_tap_dir

def DoStart(start_config, labtainer_config, lab_path, 
            quiet_start, run_container, servers, clone_count, auto_grade=False, debug_grade=False, container_images=None):
    labname = os.path.basename(lab_path)
    logger.debug("DoStart Multiple Containers and/or multi-home networking")
    ''' make sure root can access Xserver '''
    SetXhost()

    apps2start = []
    has_multi_container = CheckLabContainerApps(start_config, lab_path, apps2start)
    logger.debug("Apps to start is (%s)" % apps2start)

    hostSystem_script = os.path.join(lab_path, '*/_bin', 'hostSystemCheck.py')
    hostSystemCheckList = glob.glob('%s' % hostSystem_script)
    logger.debug("List of hostSystemCheck.py (%s)" % hostSystemCheckList)
    # If more than one hostSystemCheck.py - pick first one
    if hostSystemCheckList != [] and os.path.isfile(hostSystemCheckList[0]):
        # Do Host System Check if necessary (if file exists)
        command = "%s" % hostSystemCheckList[0]
        result = subprocess.call(shlex.split(command), stderr=subprocess.PIPE)
        if result == FAILURE:
            logger.warning("Host System Check indicates error encountered")
            if sys.version_info >=(3,0):
                user_input=input("Would you like to quit? (yes/no)\n")
            else:
                user_input=raw_input("Would you like to quit? (yes/no)\n")
            user_input=user_input.strip().lower()
            #print "user_input (%s)" % user_input
            if user_input == "yes":
                sys.exit(1)

    # Create SUBNETS
    if CreateSubnets(start_config):
        ''' don't create tapped containers until tap is ready '''
        tap_lock_dir = GetWaitTapDir()
        lock = os.path.join(tap_lock_dir, 'lock')
        try:
            os.rmdir(lock)
        except:
            pass
        try:
            os.makedirs(tap_lock_dir)
        except:
            pass
        
    student_email = None
    threads = []
    results = []
    if has_multi_container:
        container_warning_printed = False
    start_config, student_email = CheckEmailReloadStartConfig(start_config, quiet_start, lab_path, 
                                      labtainer_config, logger, servers, clone_count)    
    for name, container in start_config.containers.items():
        if SkipContainer(run_container, name, start_config, servers):
            #print('gonna skip %s' % run_container)
            continue

        if has_multi_container and container_warning_printed == False:
            print("Starting the lab, this may take a moment...")
            container_warning_printed = True
        image_info = None
        if container_images is not None:
            image_info = container_images[name]
        t = threading.Thread(target=DoStartOne, args=(labname, name, container, start_config, labtainer_config, lab_path, 
              student_email, quiet_start, results, auto_grade, image_info))
        threads.append(t)
        t.setName(name)
        t.start()
    logger.debug('started all')
    for t in threads:
        t.join()
        logger.debug('joined %s' % t.getName())

    if False in results:
        DoStop(start_config, labtainer_config, lab_path, False, run_container, servers)
        logger.error('DoStartOne has at least one failure!')
        sys.exit(1)


    readFirst(lab_path, labname, 'read_first.txt', quiet_start)
    
    DoTerminals(start_config, lab_path, run_container=run_container, servers=servers)
                
    if apps2start != [] and not auto_grade:
        print("Please wait for the apps (%s) to launch" % apps2start)

    return 0

def terminalCounter(terminal_count):
    columns = 100
    lines = 25
    x_coordinate = columns + ( 50 * terminal_count )
    y_coordinate = 75 + ( 50 * terminal_count)
    terminal_location = "--geometry %dx%d+%d+%d" % (columns, lines, x_coordinate, y_coordinate)
    return terminal_location, columns, lines

def terminalWideCounter(terminal_count):
    x_coordinate = 100 + ( 50 * terminal_count )
    y_coordinate = 75 + ( 50 * terminal_count)
    terminal_location = "--geometry 160x35+%d+%d" % (x_coordinate, y_coordinate)
    return terminal_location

# Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
def CreateHostHomeXfer(host_xfer_dir):
    # remove trailing '/'
    host_xfer_dir = host_xfer_dir.rstrip('/')
    logger.debug("host_home_xfer directory (%s)" % host_xfer_dir)
    if os.path.exists(host_xfer_dir):
        # exists but is not a directory
        if not os.path.isdir(host_xfer_dir):
            # remove file then create directory
            os.remove(host_xfer_dir)
            os.makedirs(host_xfer_dir)
        #else:
        #    logger.debug("host_home_xfer directory (%s) exists" % host_xfer_dir)
    else:
        # does not exists, create directory
        os.makedirs(host_xfer_dir)

# CopyChownGradesFile
def CopyChownGradesFile(start_config, labtainer_config, name, container_name, container_user, ignore_stop_error):
    host_home_xfer = os.path.join(labtainer_config.host_home_xfer, start_config.labname)
    labname = start_config.labname

    username = getpass.getuser()

    # Copy <labname>.grades.txt file
    grade_filename = '/home/%s/%s.grades.txt' % (container_user, labname)
    command = "docker cp %s:%s /home/%s/%s" % (container_name, grade_filename, username, host_home_xfer)
    logger.debug("Command to execute is (%s)" % command)
    result = subprocess.call(shlex.split(command))
    logger.debug("Result of subprocess.Popen exec cp %s.grades.txt file is %s" % (labname, result))
    if result == FAILURE:
        # try grabbing instructor.log
        command = "docker cp %s:/tmp/instructor.log /tmp/instructor.log" % (container_name)
        result = subprocess.call(shlex.split(command))
        logger.debug("Result of subprocess.Popen exec cp instructor.log file is %s" % (result))


        clone_names = GetContainerCloneNames(start_config.containers[name])
        for clone_full in clone_names:
            StopMyContainer(clone_full, ignore_stop_error)
            if ignore_stop_error:
                logger.debug("Container %s fail on executing cp %s.grades.txt file!\n" % (container_name, labname))
            else:
                logger.warning("Container %s fail on executing cp %s.grades.txt file!\n" % (container_name, labname))
        return


    # Copy <labname>.grades.json file
    gradejson_filename = '/home/%s/%s.grades.json' % (container_user, labname)
    command = "docker cp %s:%s /home/%s/%s" % (container_name, gradejson_filename, username, host_home_xfer)
    logger.debug("Command to execute is (%s)" % command)
    result = subprocess.call(shlex.split(command))
    logger.debug("Result of subprocess.Popen exec cp %s.grades.json file is %s" % (labname, result))
    if result == FAILURE:
        clone_names = GetContainerCloneNames(container)
        for clone_full in clone_names:
            StopMyContainer(clone_full, ignore_stop_error)
            if ignore_stop_error:
                logger.debug("Container %s fail on executing cp %s.grades.json file!\n" % (container_name, labname))
            else:
                logger.warning("Container %s fail on executing cp %s.grades.json file!\n" % (container_name, labname))
        return

def StartLab(lab_path, force_build=False, is_redo=False, quiet_start=False,
             run_container=None, servers=None, clone_count=None, auto_grade=False, debug_grade=False):
    labname = os.path.basename(lab_path)
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    logger.debug("current working directory for %s" % mycwd)
    logger.debug("current user's home directory for %s" % myhomedir)
    logger.debug("ParseStartConfig for %s" % labname)
    isValidLab(lab_path)

    lab_count = LabCount.addCount('./', labname, is_redo, logger)
    if lab_count == 1:
        readFirst(lab_path, labname, 'read_pre.txt', quiet_start, bail_option=True)
    labtainer_config, start_config = GetBothConfigs(lab_path, logger, servers, clone_count)
    host_home_xfer = os.path.join(labtainer_config.host_home_xfer, labname)

    LABS_DIR = os.path.abspath('../../labs')
    didfix = False
    ''' hackey assumption about running from labtainers-student or labtainers-instructor '''
    container_bin = './bin'
    if is_redo or force_build:
        my_start_config = os.path.join('./.tmp',labname, 'start.config')
        if os.path.isfile(my_start_config):
            logger.debug('Cached start.config removed %s' % my_start_config)
            os.remove(my_start_config)
       
    container_images = {} 
    for name, container in start_config.containers.items():
        if SkipContainer(run_container, name, start_config, servers):
            #print('skipping name %s %s' % (name, start_config.containers[name]))
            continue
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        if is_redo:
            # If it is a redo then always remove any previous container
            # If it is not a redo, i.e., start.py then DO NOT remove existing container
            clone_names = GetContainerCloneNames(container)
            for clone_full in clone_names:
                cmd = 'docker rm %s' % clone_full
                ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                output = ps.communicate()
                logger.debug("Command was (%s)" % cmd)
                if len(output[1]) > 0:
                    logger.debug("Error from command = '%s'" % str(output[1].decode('utf-8')))
        #image_exists, result, dumb = ImageExists(mycontainer_image_name, container.registry)
        if container.registry == labtainer_config.test_registry:
            branch, container_registry = registry.getBranchRegistry()
            base_registry = container_registry
        else:
            container_registry = container.registry
            base_registry = container.base_registry
        image_info = imageInfo(mycontainer_image_name, container_registry, base_registry, labtainer_config, quiet=quiet_start)
        container_images[name] = image_info
        if image_info is not None:
            logger.debug('Image version %s  framework_version %s' % (image_info.version, framework_version))
            if image_info.version is not None and int(image_info.version) > framework_version:
                print('**** Labtainer update required *****')
                print('This lab requires that you update your labtainers installation.')
                print('Please type:  update-labtainer.sh')
                print('and then try starting the lab again.') 
                exit(0)
            if not image_info.local:
                dockerPull(container_registry, mycontainer_image_name)
        else:
            logger.error('Could not find image info for %s' % name)
            exit(1)

    # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
    host_xfer_dir = '%s/%s' % (myhomedir, host_home_xfer)
    CreateHostHomeXfer(host_xfer_dir)

    DoStart(start_config, labtainer_config, lab_path, quiet_start, 
            run_container, servers=servers, clone_count=clone_count, auto_grade=auto_grade, 
            debug_grade=debug_grade, container_images=container_images)

def dumb():
    pass
    '''
    '''
def RedoLab(lab_path, force_build=False, is_redo=False, quiet_start=False,
             run_container=None, servers=None, clone_count=None, auto_grade=False, debug_grade=False):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    # Pass 'True' to ignore_stop_error (i.e., ignore certain error encountered during StopLab
    #                                         since it might not even be an error)
    lab_list, dumb = GetListRunningLabType()
    if len(lab_list) > 0:
        StopLab(lab_path, True)
    is_redo = True
    StartLab(lab_path, force_build, is_redo=is_redo, quiet_start=quiet_start,
             run_container=run_container, servers=servers, clone_count=clone_count, auto_grade=auto_grade, debug_grade=debug_grade)

def CheckShutdown(lab_path, name, container_name, container_user, ignore_stop_error):
    ''' NOT USED at the moment '''
    done = False
    count = 0
    while not done:
        command='docker cp %s:/tmp/.shutdown_done /tmp/' % (container_name)
        logger.debug(command)
        child = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        error = child.stderr.read().decode('utf-8').strip()
        if len(error) > 0:
           logger.debug("response from docker cp %s" % error)
           time.sleep(1)
        else:
           logger.debug("must have found the shutdown_done file")
           done = True
        count += 1
        if count > 5:
           done = True

def PreStop(container_name, ts):
    logger.debug("About to call prestop")
    cmd_path = '$HOME/.local/bin/prestop'
    cmd = "docker exec %s bash -c 'ls -l %s'" % (container_name, cmd_path)

    if DockerCmd(cmd, noloop=True):
        cmd = "docker exec %s bash -c '%s >$HOME/.local/result/prestop.stdout.%s'" % (container_name, cmd_path, ts)
        DockerCmd(cmd, noloop=True)

def GatherOtherArtifacts(lab_path, name, container_name, container_user, container_password, ignore_stop_error):
    '''
    Parse the results.config file looking for files named by absolute paths,
    and copy those into the .local/result directory, maintaining the original
    directory structure, e.g., .local/result/var/log/foo.log
    '''
    config_path       = os.path.join(lab_path,"instr_config") 
    results_config_path = os.path.join(config_path,"results.config")
    did_file = []
    CopyAbsToResult(container_name, '/root/.bash_history', container_user, ignore_stop_error) 
    did_file.append('/root/.bash_history')
    with open (results_config_path) as fh:
        for line in fh:
            ''' container:filename is between "=" and first " : " '''
            line = line.strip()
            if line.startswith('#') or len(line) == 0:
                continue
            if '=' not in line:
                logger.warning('no = in line %s' % line)
                continue
            after_equals = line.split('=', 1)[1].strip()
            # note assumes field delimeters are space-:-space, vice container:file 
            fname = after_equals.split(' : ')[0].strip()
            is_mine = False
            if ':' in fname:
                '''
                [container_name:]<prog>.[stdin | stdout] | [container_name:]file_path[:time_program]
 
                '''
                f_container = None
                parts = fname.split(':')
                if len(parts) == 2:
                    if parts[0].startswith('/'):
                        filename =  parts[0]
                    else:
                        f_container = parts[0]
                        filename = parts[1]
                elif len(parts) == 3:
                    f_container = parts[0]
                    filename = parts[1]
                if f_container is not None and f_container.strip() == name:
                    is_mine = True 
                filename = filename.strip()
            else: 
                is_mine = True
                filename = fname
            if is_mine:
                if filename.startswith('/') and filename not in did_file:
                    ''' copy from abs path to ~/.local/result ''' 
                    logger.debug('file on this container to copy <%s>' % filename )
                    CopyAbsToResult(container_name, filename, container_user, ignore_stop_error) 
                    did_file.append(filename)
                        
def CopyAbsToResult(container_name, fname, container_user, ignore_stop_error):
    ''' copy from abs path to ~/.local/result '''

    command='docker exec %s mkdir -p /home/%s/.local/result' % (container_name, container_user)
    command='docker exec %s sudo  cp --parents %s /home/%s/.local/result' % (container_name, fname, container_user)
    logger.debug(command)
    child = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = child.stderr.read().decode('utf-8').strip()
    if len(error) > 0:
        if ignore_stop_error:
            logger.debug('error from docker: %s' % error)
            logger.debug('command was %s' % command)
        else:
            logger.debug('error from docker: %s' % error)
            logger.debug('command was %s' % command)
    #command='docker exec %s echo "%s\n" | sudo -S chmod a+r -R /home/%s/.local/result' % (container_name, container_password, container_user)
    command='docker exec %s sudo chmod a+r -R /home/%s/.local/result' % (container_name, container_user)
    child = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = child.stderr.read().decode('utf-8').strip()
    if len(error) > 0:
        if ignore_stop_error:
            logger.debug('chmod ERROR: %s' % error)
            logger.debug('command was %s' % command)
        else:
            logger.error('chmod ERROR: %s' % error)
            logger.error('command was %s' % command)


def CreateCopyChownZip(start_config, labtainer_config, name, container_name, container_image, container_user, 
                       container_password, ignore_stop_error, keep_running, running_container=None):
    '''
    Zip up the student home directory and copy it to the Linux host home directory
    '''
    logger.debug('in CreateCopyChownZip')
    if running_container is None:
        running_container = container_name
    host_home_xfer  = os.path.join(labtainer_config.host_home_xfer, start_config.labname)

    # Run 'Student.py' - This will create zip file of the result
    logger.debug("About to call Student.py")
    ''' Copy the Student.py on each stop to handle cases where the parameter list changes.'''
    cmd = 'docker cp lab_bin/Student.py  %s:/home/%s/.local/bin/' % (running_container, container_user)
    if not DockerCmd(cmd):
        logger.error('failed to copy Student.py')
    cmd_path = '/home/%s/.local/bin/Student.py' % (container_user)
    #command=['docker', 'exec', '-i',  container_name, 'echo "%s\n" |' % container_password, '/usr/bin/sudo', cmd_path, container_user, container_image]
    command=['docker', 'exec', '-i',  running_container, '/usr/bin/sudo', cmd_path, container_user, container_image, str(keep_running)]
    logger.debug('cmd: %s' % str(command))
    child = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = child.communicate()
    if keep_running and len(output[0].strip()) > 0:
        print('\n<<<<< You may need to stop: %s in order to obtain a complete assessment. >>>>>\n' % output[0].decode('utf-8').strip())
    if len(output[1].strip()) > 0:
        if ignore_stop_error:
            logger.debug("Container %s fail on executing Student.py %s \n" % (running_container, output[1].decode('utf-8')))
        else:
            logger.error("Container %s fail on executing Student.py %s \n" % (running_container, output[1].decode('utf-8')))
        return None, None
    logger.debug("results from Student.py: %s" % output[0].decode('utf-8'))
    
    #out_string = output[0].strip()
    #if len(out_string) > 0:
    #    logger.debug('output of Student.py is %s' % out_string)
    username = getpass.getuser()

    tmp_dir=os.path.join('/tmp/labtainers', container_name)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    try:
        os.makedirs(tmp_dir)
    except os.error:
        logger.error("did not expect to find dir %s" % tmp_dir)
    source_dir = os.path.join('/home', container_user, '.local', 'zip')
    cont_source = '%s:%s' % (container_name, source_dir)
    logger.debug('will copy from %s ' % source_dir)
    command = ['docker', 'cp', cont_source, tmp_dir]
    # The zip filename created by Student.py has the format of e-mail.labname.zip
    logger.debug("Command to execute is (%s)" % command)
    child = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_string = child.stderr.read().decode('utf-8').strip()
    if len(error_string) > 0:
        if ignore_stop_error:
            logger.debug("Container %s fail on executing cp zip file: %s\n" % (container_name, error_string))
            logger.debug("Command was (%s)" % command)
        else:
            logger.error("Container %s fail on executing cp zip file: %s\n" % (container_name, error_string))
            logger.error("Command was (%s)" % command)
        clone_names = GetContainerCloneNames(start_config.containers[name])
        for clone_full in clone_names:
            StopMyContainer(clone_full, ignore_stop_error)
        return None, None
    
    local_tmp_zip = os.path.join(tmp_dir, 'zip')
    try:
        orig_zipfilenameext = os.listdir(local_tmp_zip)[0]
    except:
        if ignore_stop_error:
            logger.debug('no files at %s\n' % local_tmp_zip)
        else:
            logger.error('no files at %s\n' % local_tmp_zip)
        return None, None
    orig_zipfilename, orig_zipext = os.path.splitext(orig_zipfilenameext)
    baseZipFilename = os.path.basename(orig_zipfilename)
    #NOTE: Use the '=' to separate e-mail+labname from the container_name
    DestZipFilename = '%s=%s.zip' % (baseZipFilename, container_name)
    DestZipPath = os.path.join('/home', username, host_home_xfer, DestZipFilename)
    shutil.copyfile(os.path.join(local_tmp_zip, orig_zipfilenameext), DestZipPath)

    currentContainerZipFilename = "/home/%s/%s/%s" % (username, host_home_xfer, DestZipFilename)
    return baseZipFilename, currentContainerZipFilename
   
# Stop my_container_name container
def StopMyContainer(container_name, ignore_stop_error):
    command = "docker stop -t 1 %s" % container_name
    logger.debug("Command to execute is (%s)" % command)
    ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) > 0:
        if ignore_stop_error:
            logger.debug('Fail to stop container, error returned %s' % output[1].decode('utf-8'))
        else:
            logger.error('Fail to stop container, error returned %s' % output[1].decode('utf-8'))
    #if len(output[0].strip()) > 0:
    #    logger.debug('StopMyContainer stdout %s' % output[0])
    #result = subprocess.call(command, shell=True)

def GetContainerID(image):
    command = "docker ps"
    ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    retval = None
    if len(output[1].strip()) > 0:
        logger.error('Fail to get a list of running containers, error returned %s' % output[1].decode('utf-8'))
        
    elif len(output[0].decode('utf-8')) > 0:
        docker_ps_output = output[0].decode('utf-8').split('\n')
        for line in docker_ps_output:
            line = line.strip()
            if image in line:
                parts = line.split()
                retval = parts[0]
                break
    return retval

# Get a list of running lab names
def GetListRunningLabType():
    lablist = []
    is_gns3 = False
    # Note: doing "docker ps" not "docker ps -a" to get just the running container
    command = "docker ps"
    logger.debug("GetListRunningLab Command to execute is (%s)" % command)
    ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) > 0:
        logger.error('Fail to get a list of running containers, error returned %s' % output[1].decode('utf-8'))
        sys.exit(1)
    if len(output[0].decode('utf-8')) > 0:
        docker_ps_output = output[0].decode('utf-8').split('\n')
        for each_line in docker_ps_output:
            # Skip empty line or the "CONTAINER ID" line - the header line returned by "docker ps"
            current_line = each_line.strip()
            if not current_line or len(current_line) == 0 or current_line.startswith("CONTAINER"):
                continue
            logger.debug(current_line)
            # Assume the container name is the last token on the line
            container_info = current_line.split()
            container_name = container_info[-1]
            # And the image is the 2nd token
            image_name = container_info[1]
            image_name = os.path.basename(image_name)
            if container_name.startswith(image_name):
                ''' std Labtainers image, get is labname '''
                labname = container_name.split('.')[0]
            elif 'labtainer' in image_name:
                ''' gns3 labtainer image '''
                labname = image_name.split('_', 1)[0]
                is_gns3 = True
            else:
                logger.debug('not a labtainer: %s' % image_name)
                continue
            if labname not in lablist:
                logger.debug('appending %s' % labname)
                lablist.append(labname)
    return lablist, is_gns3

def GetListRunningLab():
    lab_list, is_gns3 = GetListRunningLabType()
    return lab_list

# Given a network name, if it is valid, get a list of labname for the container(s) that is(are)
# using that network. Note: the network name is passed in as an argument
def GetListLabContainerOnNetwork(network_name):
    containerlabnamelist = []
    command = "docker network inspect %s" % network_name
    logger.debug("Command to execute is (%s)" % command)
    ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) > 0:
        logger.error('Fail to inspect the network %s, error returned %s' % (network_name, output[1].decode('utf-8')))
        sys.exit(1)
    if len(output[0]) > 0:
        network_result = json.loads(output[0].decode('utf-8'))
        if len(network_result) != 0:
            result = network_result[0]
            containers = result["Containers"]
            for key in containers:
                container_name = containers[key]["Name"]
                # Assume the labname is the first token if split by '.'
                labname = container_name.split('.')[0]
                if labname not in containerlabnamelist:
                    containerlabnamelist.append(labname)
    return containerlabnamelist

# Given an IP address (gateway IP address) - find a network name that has that IP address as its gateway
# Note: the IP address is passed in as an argument
def FindNetworkGivenGatewayIP(gateway_address):
    found_match_network = False
    found_match_network_name = ""
    logger.debug("FindNetworkGivenGatewayIP %s" % gateway_address)
    networklist = []
    # First get a list of network name of driver=bridge
    command = "docker network ls --filter driver=bridge"
    logger.debug("Command to execute is (%s)" % command)
    ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) > 0:
        logger.error('Fail to get a list of network (driver=bridge), error returned %s' % output[1].decode('utf-8'))
        sys.exit(1)
    if len(output[0]) > 0:
        network_list = output[0].decode('utf-8').split('\n')
        for each_line in network_list:
            # Skip empty line or the "NETWORK ID" line - the header line returned by "docker network"
            current_line = each_line.strip()
            if not current_line or current_line.startswith("NETWORK"):
                continue
            # Assume the network name is the second token on the line
            container_info = current_line.split()
            network_name = container_info[1]
            # Do not need to check network name "bridge"
            if network_name != "bridge" and network_name not in networklist:
                networklist.append(network_name)
    # Loop through each network (driver=bridge) to find if any uses IP address as gateway
    for network_name in networklist:
        command = "docker network inspect %s" % network_name
        logger.debug("Command to execute is (%s)" % command)
        ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1].strip()) > 0:
            logger.error('Fail to inspect the network %s, error returned %s' % (network_name, output[1].decode('utf-8')))
            sys.exit(1)
        if len(output[0]) > 0:
            network_result = json.loads(output[0].decode('utf-8'))
            if len(network_result) != 0:
                result = network_result[0]
                ipam_config = result["IPAM"]["Config"][0]
                for key in ipam_config:
                    if key == "Gateway":
                        ipam_config_gateway_ip = ipam_config[key]
                        if gateway_address == ipam_config_gateway_ip:
                            found_match_network = True
                            found_match_network_name = network_name
                            break
    return found_match_network, found_match_network_name

# Given a subnet (network subnet) - find a network name that has that same subnet
# Note: the subnet is passed in as an argument
def FindNetworkGivenSubnet(subnet):
    found_match_network = False
    found_match_network_name = ""
    logger.debug("FindNetworkGivenSubnet %s" % subnet)
    networklist = []
    # First get a list of network name of driver=bridge
    command = "docker network ls --filter driver=bridge"
    logger.debug("Command to execute is (%s)" % command)
    ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) > 0:
        logger.error('Fail to get a list of network (driver=bridge), error returned %s' % output[1].decode('utf-8'))
        sys.exit(1)
    if len(output[0]) > 0:
        network_list = output[0].decode('utf-8').split('\n')
        for each_line in network_list:
            # Skip empty line or the "NETWORK ID" line - the header line returned by "docker network"
            current_line = each_line.strip()
            if not current_line or current_line.startswith("NETWORK"):
                continue
            # Assume the network name is the second token on the line
            container_info = current_line.split()
            network_name = container_info[1]
            # Do not need to check network name "bridge"
            if network_name != "bridge" and network_name not in networklist:
                networklist.append(network_name)
    # Loop through each network (driver=bridge) to find if any that has the same subnet
    for network_name in networklist:
        command = "docker network inspect %s" % network_name
        logger.debug("Command to execute is (%s)" % command)
        ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1].decode('utf-8').strip()) > 0:
            logger.error('Fail to inspect the network %s, error returned %s' % (network_name, output[1].decode('utf-8')))
            sys.exit(1)
        if len(output[0]) > 0:
            network_result = json.loads(output[0].decode('utf-8'))
            if len(network_result) != 0:
                result = network_result[0]
                ipam_config = result["IPAM"]["Config"][0]
                for key in ipam_config:
                    if key == "Subnet":
                        ipam_config_subnet = ipam_config[key]
                        if subnet == ipam_config_subnet:
                            found_match_network = True
                            found_match_network_name = network_name
                            break
    return found_match_network, found_match_network_name

def AllContainersRunning(container):
    clone_names = GetContainerCloneNames(container)
    for clone_full in clone_names:
        if not IsContainerRunning(clone_full):
            return False
    return True

def IsContainerRunning(mycontainer_name):
    cmd = 'docker ps -f id=%s' % mycontainer_name
    try:
        dumb = int(mycontainer_name, 16)
    except:
        cmd = 'docker ps -f name=%s' % mycontainer_name
    try:
        s = subprocess.check_output(shlex.split(cmd)).decode('utf-8')
    except:
        return False
    if mycontainer_name in s:
        return True
    else:
        return False 

def ShouldBeRunning(start_config, container):
    if start_config.multi_user is not None and start_config.multi_user != 'clones':
        if start_config.multi_user == 'server' and container.client == 'yes':
            return False
        if start_config.multi_user == 'client' and container.client != 'yes':
            return False
    return True
       
   
def DoStopOne(start_config, labtainer_config, lab_path, name, container, zip_file_list, ignore_stop_error, results, keep_running):
        labname = os.path.basename(lab_path) 
        #dumlog = os.path.join('/tmp', name+'.log')
        #sys.stdout = open(dumlog, 'w')
        #sys.stderr = sys.stdout
        retval = True
        mycontainer_name  = container.full_name
        container_user    = container.user
        container_password    = container.password
        mycontainer_image = container.image_name
        haveContainer     = AllContainersCreated(container)
        logger.debug("AllContainersCreated for %s result (%s)" % (container.name, haveContainer))

        # IsContainerCreated returned FAILURE if container does not exists
        # error: can't stop non-existent container
        if not haveContainer:
            if ShouldBeRunning(start_config, container) and not ignore_stop_error:
                logger.error("Container %s does not exist!\n" % mycontainer_name)
                retval = False

        elif container.tap == 'yes':
            StopMyContainer(mycontainer_name, ignore_stop_error)
        else:
            clone_names = GetContainerCloneNames(container)
            for mycontainer_name in clone_names:
                if not IsContainerRunning(mycontainer_name):
                    if ShouldBeRunning(start_config, container):
                        if ignore_stop_error:
                            logger.debug("container %s not running\n" % (mycontainer_name))
                        else:
                            logger.error("container %s not running\n" % (mycontainer_name))
                            retval = False
                    continue
                GatherOtherArtifacts(lab_path, name, mycontainer_name, container_user, container_password, ignore_stop_error)
                # Before stopping a container, run 'Student.py'
                # This will create zip file of the result
    
                baseZipFilename, currentContainerZipFilename = CreateCopyChownZip(start_config, labtainer_config, name, 
                             mycontainer_name, mycontainer_image, container_user, container_password, ignore_stop_error, keep_running)
                if baseZipFilename is not None:
                    if currentContainerZipFilename is not None:
                        zip_file_list.append(currentContainerZipFilename)
                    else:
                        logger.debug('currentContainerZipFilename is None for container %s' % mycontainer_name)

                    logger.debug("baseZipFilename is (%s)" % baseZipFilename)
                else:
                    logger.debug("baseZipFileName is None for container %s" % mycontainer_name)

                #command = 'docker exec %s echo "%s\n" | sudo -S rmdir /tmp/.mylockdir 2>/dev/null' % (mycontainer_name, container_password)
                command = 'docker exec %s sudo rmdir /tmp/.mylockdir 2>/dev/null' % (mycontainer_name)
                os.system(command)
                if not keep_running:
                    did_this = []
                    for mysubnet_name, mysubnet_ip in container.container_nets.items():
                        subnet_name = mysubnet_name
                        if ':' in mysubnet_name:
                            subnet_name = mysubnet_name.split(':')[0] 
                        if subnet_name not in did_this:
                            disconnectNetworkResult = DisconnectNetworkFromContainer(mycontainer_name, subnet_name)
                            did_this.append(subnet_name)

                # Stop the container
            
                if not keep_running:
                    StopMyContainer(mycontainer_name, ignore_stop_error)

        results.append(retval)

def SynchStop(start_config, run_container=None):
    threads = []
    now = datetime.datetime.now()
    ts = now.strftime('%Y%m%d%H%M%S')
    for name, container in start_config.containers.items():
        if run_container is not None and container.full_name != run_container:
            #print('not for me %s ' % run_container)
            continue
        clone_names = GetContainerCloneNames(container)
        for mycontainer_name in clone_names:
            t = threading.Thread(target=PreStop, args=[mycontainer_name, ts])
            threads.append(t)
            t.setName(name)
            t.start()
      
        logger.debug('prestop started on all')
        for t in threads:
            t.join()
            logger.debug('joined %s' % t.getName())

def GatherZips(zip_file_list, labtainer_config, start_config, labname, lab_path):
    mycwd = os.getcwd()
    if len(zip_file_list) == 0:
        logger.error('GatherZips called without any zips')
        return
    try:
        base_filename = os.path.basename(zip_file_list[0])
    except:
        logger.error('No basefile found in %s' % zip_file_list[0])
        return
    baseZipFilename = base_filename.split('=')[0]

    host_home_xfer  = os.path.join(labtainer_config.host_home_xfer, labname)
    username = getpass.getuser()
    xfer_dir = "/home/%s/%s" % (username, host_home_xfer)
    try:
        os.makedirs(xfer_dir)
    except:
        pass

    # Create docs.zip in xfer_dir if COLLECT_DOCS is "yes"
    if start_config.collect_docs.lower() == "yes":
        docs_zip_file = "%s/docs.zip" % xfer_dir
        logger.debug("Zipping docs directory to %s" % docs_zip_file)

        docs_path = '%s/docs' % lab_path
        if os.path.isdir(docs_path):
            docs_zip_filelist = glob.glob('%s/*' % docs_path)
            logger.debug(docs_zip_filelist)

            # docs.zip file
            docs_zipoutput = zipfile.ZipFile(docs_zip_file, "w")
            # Go to the docs_path
            os.chdir(docs_path)
            for docs_fname in docs_zip_filelist:
                docs_basefname = os.path.basename(docs_fname)
                docs_zipoutput.write(docs_basefname, compress_type=zipfile.ZIP_DEFLATED)
                # Note: DO NOT remove after the file is zipped
            docs_zipoutput.close()

            # Add docs.zip into the zip_file_list
            zip_file_list.append(docs_zip_file)
        else:
            logger.debug('no docs at %s' % docs_path)

    # Combine all the zip files
    logger.debug("zip_file_list is ")
    logger.debug(zip_file_list)
    logger.debug("baseZipFilename is (%s)" % baseZipFilename)
    combinedZipFilename = "%s/%s.zip" % (xfer_dir, baseZipFilename)
    logger.debug("The combined zip filename is %s" % combinedZipFilename)
    zipoutput = zipfile.ZipFile(combinedZipFilename, "w")
    # Go to the xfer_dir
    os.chdir(xfer_dir)
    for fname in zip_file_list:
        basefname = os.path.basename(fname)
        zipoutput.write(basefname, compress_type=zipfile.ZIP_DEFLATED)
        # Remove after the file is zipped
        os.remove(basefname)

    # Add count.json and labtainer.log (if they exist) to the zip file
    count_path = LabCount.getPath('./', labname)
    #print "count_path is %s" % count_path
    if os.path.isfile(count_path):
        parent = os.path.dirname(count_path)
        os.chdir(mycwd)
        os.chdir(parent)
        fname = os.path.join('./', os.path.basename(count_path))
        zipoutput.write(fname, compress_type=zipfile.ZIP_DEFLATED)
    os.chdir(mycwd)
    my_labtainer_log = os.path.join('./', 'labtainer.log')
    if os.path.exists(my_labtainer_log):
        zipoutput.write(my_labtainer_log, compress_type=zipfile.ZIP_DEFLATED)

    zipoutput.close()
    post_zip = os.path.join(lab_path, 'bin', 'postzip')
    if os.path.isfile(post_zip):
         cmd = "%s %s" % (post_zip, combinedZipFilename)
         os.system(cmd)
    os.chdir(mycwd)


def DoStop(start_config, labtainer_config, lab_path, ignore_stop_error, run_container=None, servers=None, clone_count=None, keep_running=False):
    retval = True
    labname = os.path.basename(lab_path)
    logger.debug("DoStop Multiple Containers and/or multi-home networking, keep_running is %r" % keep_running)
    SynchStop(start_config, run_container)

    baseZipFilename = ""
    zip_file_list = []
    threads = []
    results = []
    for name, container in start_config.containers.items():
        if run_container is not None and container.full_name != run_container:
            #print('not for me %s ' % run_container)
            continue
        mycontainer_name = '%s.%s.student' % (labname, container.name)

        t = threading.Thread(target=DoStopOne, args=(start_config, labtainer_config, lab_path, 
              name, container, zip_file_list, ignore_stop_error, results, keep_running))
        threads.append(t)
        t.setName(name)
        t.start()
      
    logger.debug('stopped all')
    for t in threads:
        t.join()
        logger.debug('joined %s' % t.getName())

    if not keep_running:
        RemoveSubnets(start_config.subnets, ignore_stop_error)
    if not ignore_stop_error:
        if False in results:
            logger.error('DoStopOne has at least one failure!')
            sys.exit(1)

    if len(zip_file_list) == 0:
        if ignore_stop_error:
            logger.debug('No zip files found')
        else:
            logger.error('No zip files found')
        return None
    ''' Check for empty email identifier '''
    if zip_file_list[0].startswith('.'):
        lgr.error('Missing email for student, cannot gather artifacts')
        return None
    GatherZips(zip_file_list, labtainer_config, start_config, labname, lab_path)
    return retval

# ignore_stop_error - set to 'False' : do not ignore error
# ignore_stop_error - set to 'True' : ignore certain error encountered since it might not even be an error
#                                     such as error encountered when trying to stop non-existent container
def StopLab(lab_path, ignore_stop_error, run_container=None, servers=None, clone_count=None, keep_running=False):
    labname = os.path.basename(lab_path)
    myhomedir = os.environ['HOME']
    logger.debug("keep_running is %r" % keep_running)
    logger.debug("ParseStartConfig for %s" % labname)
    isValidLab(lab_path)
    labtainer_config, start_config = GetBothConfigs(lab_path, logger, servers, clone_count)
    host_home_xfer = os.path.join(labtainer_config.host_home_xfer, labname)

    # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
    host_xfer_dir = '%s/%s' % (myhomedir, host_home_xfer)
    CreateHostHomeXfer(host_xfer_dir)

    if DoStop(start_config, labtainer_config, lab_path, ignore_stop_error, run_container=run_container, 
              servers=servers, clone_count=clone_count, keep_running=keep_running):
        # Inform user where results are stored
        print("Results stored in directory: %s" % host_xfer_dir)
    return host_xfer_dir

def DoMoreterm(lab_path, container_name, clone_num=None, alt_name=None):
    labname = os.path.basename(lab_path)
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    isValidLab(lab_path)
    labtainer_config, start_config = GetBothConfigs(lab_path, logger)
    if container_name not in start_config.containers:
        logger.error("Container %s not found. Container must be one of the following:" % container_name)
        for container_name in start_config.containers:
            print('\t%s' % container_name)
        print("Usage: moreterm.py <lab> <container>")
        return False
        
    logger.debug('num terms is %d' % start_config.containers[container_name].terminals)
    if clone_num is None:
        mycontainer_name = '%s.%s.student' % (labname, container_name)
    else:
        mycontainer_name = '%s.%s-%d.student' % (labname, container_name, clone_num)

    if alt_name is not None:
        mycontainer_name = alt_name

    if not IsContainerCreated(mycontainer_name):
        logger.error('DoMoreTerm container %s not found' % mycontainer_name)
        sys.exit(1)
    if not IsContainerRunning(mycontainer_name):
        logger.error("Container %s is not running!\n" % (mycontainer_name))
        sys.exit(1)

    if start_config.containers[container_name].terminals == -1:
        logger.debug("No terminals supported for %s" % container_name)
        return False
    else:
        spawn_command = "gnome-terminal -- docker exec -it %s bash -l &" % 	mycontainer_name
        logger.debug("spawn_command is (%s)" % spawn_command)
        os.system(spawn_command)
    return True

def DoTransfer(lab_path, container_name, filename, direction):
    '''TBD this is not tested and likey broken'''
    labname = os.path.basename(lab_path)
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    logger.debug("current working directory for %s" % mycwd)
    logger.debug("current user's home directory for %s" % myhomedir)
    logger.debug("ParseStartConfig for %s" % labname)
    isValidLab(lab_path)
    labtainer_config, start_config = GetBothConfigs(lab_path, logger)
    host_home_xfer = os.path.join(labtainer_config.host_home_xfer, labname)
    logger.debug('num terms is %d' % start_config.containers[container_name].terminals)
    host_xfer_dir = '%s/%s' % (myhomedir, host_home_xfer)

    mycontainer_name = '%s.%s.student' % (labname, container_name)
    if not IsContainerCreated(mycontainer_name):
        logger.error('container %s not found' % mycontainer_name)
        sys.exit(1)
    if not IsContainerRunning(mycontainer_name):
        logger.error("Container %s is not running!\n" % (mycontainer_name))
        sys.exit(1)
    container_user = ""
    for name, container in start_config.containers.items():
        if mycontainer_name == container.full_name:
            container_user = container.user

    if direction == "TOCONTAINER":
        # Transfer from host to container
        filename_path = '%s/%s' % (host_xfer_dir, filename)
        logger.debug("File to transfer from host is (%s)" % filename_path)
        if os.path.exists(filename_path) and os.path.isfile(filename_path):
            # Copy file and chown it
            command = 'docker cp %s %s:/home/%s/' % (filename_path, mycontainer_name, container_user)
            logger.debug("Command to execute is (%s)" % command)
            result = subprocess.call(command, shell=True)
            logger.debug("Result of subprocess.call DoTransfer copy (TOCONTAINER) file (%s) is %s" % (filename_path, result))
            if result == FAILURE:
                logger.error("Failed to copy file to container %s!\n" % mycontainer_name)
                sys.exit(1)
            command = 'docker exec %s sudo chown %s:%s /home/%s/%s' % (mycontainer_name, container_user, container_user, container_user, filename)
            logger.debug("Command to execute is (%s)" % command)
            result = subprocess.call(command, shell=True)
            logger.debug("Result of subprocess.call DoTransfer chown file (%s) is %s" % (filename_path, result))
            if result == FAILURE:
                logger.error("Failed to set permission in container %s!\n" % mycontainer_name)
                sys.exit(1)
        else:
            logger.error('Host does not have %s file' % filename_path)
            sys.exit(1)
    else:
        # Transfer from container to host
        command = 'docker cp %s:/home/%s/%s %s/' % (mycontainer_name, container_user, filename, host_xfer_dir)
        logger.debug("Command to execute is (%s)" % command)
        result = subprocess.call(command, shell=True)
        logger.debug("Result of subprocess.call DoTransfer copy (TOHOST) file (%s) is %s" % (filename, result))
        if result == FAILURE:
            logger.error("Failed to copy file from container %s!\n" % mycontainer_name)
            sys.exit(1)


def CopyFilesToHost(lab_path, container_name, full_container_name, container_user):
    labname = os.path.basename(lab_path)
    isValidLab(lab_path)
    config_path       = os.path.join(lab_path,"config") 
    copy_path = os.path.join(config_path,"files_to_host.config")
    logger.debug('CopyFilesToHost %s %s %s' % (labname, container_name, full_container_name))
    logger.debug('CopyFilesToHost copypath %s' % copy_path)
    if os.path.isfile(copy_path):
        with open(copy_path) as fh:
            for line in fh:
                if not line.strip().startswith('#'):
                    try:
                        os.mkdir(os.path.join(os.getcwd(), labname))
                    except OSError as e:
                        #logger.error('could not mkdir %s in %s %s' % (labname, os.getcwd(),str(e)))
                        pass
                    container, file_name = line.split(':')                    
                    if container == container_name:
                        dest = os.path.join(os.getcwd(), labname, file_name)
                        command = 'docker cp %s:/home/%s/%s %s' % (full_container_name, container_user, 
                            file_name.strip(), dest)
                        logger.debug("Command to execute is (%s)" % command)
                        result = subprocess.call(command, shell=True)
                        logger.debug("Result of subprocess.call DoTransfer copy (TOHOST) file (%s) is %s" % (file_name, 
                            result))
                        if result == FAILURE:
                            logger.error("Failed to copy file from container %s!\n" % full_container_name)
                            sys.exit(1)

def GetContainerId(image):
    command = "docker ps"
    logger.debug("Command to execute is (%s)" % command)
    ps = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) > 0:
        logger.error('GetContainerId, Failed to get a list of running containers, error returned %s' % output[1].decode('utf-8'))
        sys.exit(1)
    if len(output[0]) > 0:
        docker_ps_output = output[0].decode('utf-8').splitlines()
        for each_line in docker_ps_output:
            # Skip empty line or the "CONTAINER ID" line - the header line returned by "docker ps"
            current_line = each_line.strip()
            parts = current_line.split()
            if parts[1].startswith(image):
               return parts[0]
    return None
