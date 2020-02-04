#!/usr/bin/env python3
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
'''
Intended to be run as a service on a Labtainers VM, return status of running lab exercise
and allow execution of a copy directive defined in the given lab's config/copy.config file.
'''
import subprocess
import os
import sys
import socket
import argparse
labtainer_dir = os.getenv('LABTAINER_DIR')
if labtainer_dir is None:
    print('LABTAINER_DIR not defined')
    exit(1)
lab_bin = os.path.join(labtainer_dir,'scripts', 'labtainer-student', 'bin')
sys.path.append(lab_bin)
import labutils
import LabtainerLogging
PORT = 60000

class CopyDirective():
    def __init__(self, line, labdir):
        parts = line.split()
        self.name = parts[0]
        self.container = parts[1]
        self.source = parts[2]
        if parts[2].startswith('$'):
            rest = parts[2][5:]
            self.source = os.path.join(labdir, rest)
        self.dest = parts[3]

def getRunningLab():
    labs, is_gns3 = labutils.GetListRunningLabType()
    retval = None
    if len(labs) == 0:
        #print('No labs have started')
        pass
    elif len(labs) == 1:
        print('Lab is %s' % labs[0])
        retval = labs[0]
    else:
        print('Multiple labs running?')
    return retval, is_gns3

def getContainer(lab_path, container_name, is_gns3, logger):
    labname = os.path.basename(lab_path)
    labtainer_config, start_config = labutils.GetBothConfigs(lab_path, logger)
    retval = None
    if container_name in start_config.containers:
        if is_gns3:
            image = '%s_%s-labtainer' % (labname, container_name)
        else:
            image = '%s.%s.student' % (labname, container_name)
        retval = labutils.GetContainerID(image)
    return retval

def doCopy(copy_directive, labdir, is_gns3, logger):
    copy_config = os.path.join(labdir, 'config', 'copy.config')
    the_directive = None
    retval = None
    if os.path.isfile(copy_config):
        with open(copy_config) as fh:
            for line in fh:
                if not line.strip().startswith('#'):
                    parts = line.split()
                    if len(parts) != 4:
                        logger.error('Bad directive in %s\%s' % (copy_config, line))
                        return False 
                    if parts[0] == copy_directive:
                        the_directive = CopyDirective(line, labdir)
                        break 
    else:
        retval = 'Missing %s' % copy_config
    if the_directive is not None:
        container = getContainer(labdir, the_directive.container, is_gns3, logger)
        cmd = 'docker cp %s %s:%s' % (the_directive.source, container, the_directive.dest)
        #print('cmd is %s' % cmd)
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1].strip()) > 0:
            logger.error(output[1].decode('utf-8'))
            retval = output[1].decode('utf-8')
        else:
            retval = 'Copy of %s complete' % the_directive.source
    else:
        retval = 'No directive found: %s' % copy_directive
    return retval

def daemon(logger):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_addr = ('192.168.122.1', 6000)
    server_addr = ('0.0.0.0', PORT)
    print('do bind')
    sock.bind(server_addr)
    sock.listen()
    while True:
        conn, src_addr = sock.accept()
        with conn:
            got, addr = conn.recvfrom(4096)
   
            if got is None or len(got) == 0:
                print('got zilch, quit')
                conn.close()
            else:
                got = got.decode()
                print('got %s' % got)
                if got.strip() == 'status':
                    lab, is_gns3 = getRunningLab()
                    if lab is not None:
                        conn.sendall(lab.encode())
                    else:
                        conn.sendall(b'No lab is running.')
                elif got.strip().startswith('copy'):
                    parts = got.split() 
                    if len(parts) == 3:
                        labdir = None
                        lab = parts[1]
                        running, is_gns3 = getRunningLab()
                        if lab == running:
                            labdir = os.path.abspath(os.path.join(labtainer_dir,  'labs', lab))
                            result = doCopy(parts[2], labdir, is_gns3, logger)
                            conn.sendall(result.encode())
                        elif running is not None:
                            conn.sendall(b'Wrong lab, found %s, asked for %s' % (running, args.lab))
                        else:
                            conn.sendall(b'No lab is running.')
                else:
                    conn.sendall(b'Unknown command: %s' % got.decode())
                conn.close()


if __name__ == '__main__':
    labtainer_config_file = os.path.join(labtainer_dir, 'config', 'labtainer.config')
    logger = LabtainerLogging.LabtainerLogging("/tmp/remote.log", 'publish', labtainer_config_file)
    labutils.logger = logger

    parser = argparse.ArgumentParser(description='Display and alter state of a Labtainer exercise')
    parser.add_argument('-l', '--lab', action='store', help='manage this lab')
    parser.add_argument('-c', '--copy', action='store', help='Copy files per the named directive.')
    parser.add_argument('-s', '--status', action='store_true', default=False, help='status of lab on this VM')
    parser.add_argument('-d', '--daemon', action='store_true', default=False, help='Run as daemon listening on port %d' % PORT)
    args = parser.parse_args()
    if args.daemon:
        daemon(logger)
    else:
        if args.status:
            lab, is_gns3 = getRunningLab()
            if lab is not None:
                print('Running lab: %s' % lab)
            else:
                print('No lab is running.')           
        labdir = None
        if args.lab is not None: 
            running, is_gns3 = getRunningLab()
            if args.lab == running:
                labdir = os.path.abspath(os.path.join(labtainer_dir,  'labs', args.lab))
            elif running is not None:
                print('Wrong lab, found %s, asked for %s' % (running, args.lab))
        if args.copy is not None: 
            doCopy(args.copy, labdir, is_gns3, logger) 
