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
import sys
import os
import labutils
import logging
import LabtainerLogging
import argparse
import CurrentLab

try:
    from dateutil import parser
except:
    print('Lab building now requires a python3 environment with includes dateutil')
    print('Please migrate to a newer Linux distribution, e.g, Ubuntu 18')
    print('As a short-term work-around, use the rebuild command (no .py suffix) to reference python2')
    print('Avoid use of python 3.5.2, it is broken, see our README.')
    exit(1)

# Usage: redo.py <labname> [-f]
# Arguments:
#    <labname> - the lab to stop, delete and start
#    [-f] will force a rebuild
#    [-q] will load the lab using a predetermined email.
def main():
    parser = argparse.ArgumentParser(description='Build the images of a lab and start the lab.',prog='rebuild')
    parser.add_argument('labname', help='The lab to build')
    parser.add_argument('-f', '--force', action='store_true', help='Force build of all containers in the lab.')
    parser.add_argument('-p', '--prompt', action='store_true', help='prompt for email, otherwise use stored')
    parser.add_argument('-C', '--force_container', action='store', help='force rebuild just this container')
    parser.add_argument('-o', '--only_container', action='store', help='run only this container')
    parser.add_argument('-t', '--test_registry', action='store_true', default=False, help='build from images in the test registry')
    parser.add_argument('-s', '--servers', action='store_true', help='Start containers that are not clients -- intended for distributed Labtainers')
    parser.add_argument('-w', '--workstation', action='store_true', help='Intended for distributed Labtainers, start the client workstation.')
    parser.add_argument('-n', '--client_count', action='store', help='Number of clones of client containers to create, intended for multi-user labs')
    parser.add_argument('-L', '--no_pull', action='store_true', default=False, help='Local building, do not pull from internet')

    args = parser.parse_args()
    quiet_start = True
    if args.prompt == True:
        quiet_start = False
    if args.force is not None:
        force_build = args.force
    #print('force %s quiet %s container %s' % (force_build, quiet_start, args.container))
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", args.labname, "../../config/labtainer.config")
    labutils.logger.info("Begin logging Rebuild.py for %s lab" % args.labname)
    lab_path = os.path.join(os.path.abspath('../../labs'), args.labname)

    if args.test_registry:
        if os.getenv('TEST_REGISTRY') is None:
            #print('use putenv to set it')
            os.putenv("TEST_REGISTRY", "TRUE")
            ''' why does putenv not set the value? '''
            os.environ['TEST_REGISTRY'] = 'TRUE'
        else:
            #print('exists, set it true')
            os.environ['TEST_REGISTRY'] = 'TRUE'
        print('set TEST REG to %s' % os.getenv('TEST_REGISTRY'))

    distributed = None
    if args.servers and args.workstation:
        print('--server and --workstation are mutually exclusive')
        exit(1)
    elif args.servers: 
        distributed = 'server' 
    elif args.workstation:
        distributed = 'client'
    labutils.RebuildLab(lab_path, force_build=force_build, quiet_start=quiet_start, 
          just_container=args.force_container, run_container=args.only_container, servers=distributed, clone_count=args.client_count, no_pull=args.no_pull)
    current_lab = CurrentLab.CurrentLab()
    current_lab.add('lab_name', args.labname)
    current_lab.add('clone_count', args.client_count)
    current_lab.add('servers', distributed)
    current_lab.save()

    return 0

if __name__ == '__main__':
    sys.exit(main())

