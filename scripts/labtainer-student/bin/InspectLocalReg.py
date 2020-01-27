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
import os
import sys
import json
import subprocess
import VersionInfo
'''
Return creation date and user of a given image from a local registry, i.e.,
the test registry.
'''



def inspectLocal(image, lgr, test_registry, is_rebuild=False, quiet=False, no_pull=False):
    use_tag = 'latest'
    lgr.debug('inspectLocal image %s' % image)
    digest = getDigest(image, 'latest', test_registry)
    if digest is None:
        return None, None, None, None, None
    lgr.debug('inspectLocal digest %s' % digest)
    created, user, version, base = getCreated(image, digest, test_registry)
    #print('base is %s' % base)
    
    if not no_pull and base is not None:
       base_image, base_id = base.rsplit('.', 1)
       my_id = VersionInfo.getImageId(base_image, quiet)
       if my_id == base_id:
           pass
           #print('got correct base_id')
       else:
            print('got WRONG base_id for base %s used in  %s my: %s  base: %s' % (base_image, image, my_id, base_id))
            tlist = getTags(image, test_registry)
            need_tag = 'base_image%s' % my_id
            if is_rebuild or need_tag in tlist:
                use_tag = need_tag
            elif quiet:
                cmd = 'docker pull %s' % base_image
                os.system(cmd)
            else:
                print('**************************************************')
                print('*  This lab will require a download of           *')
                print('*  several hundred megabytes.                    *')
                print('**************************************************')
                if sys.version_info >=(3,0):
                    confirm = str(input('Continue? (y/n)')).lower().strip()
                else:
                    confirm = str(raw_input('Continue? (y/n)')).lower().strip()
                if confirm != 'y':
                    print('Exiting lab')
                    exit(0)
                else:
                    print('Please wait for download to complete...')
                    cmd = 'docker pull %s' % base_image
                    os.system(cmd)
                    print('Download has completed.  Wait for lab to start.')

    return created, user, version, use_tag, base

def checkRegistryExists(test_registry, lgr):
    cmd = 'curl http://%s/v2/' % test_registry
    retval = True
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0]) > 0:
        val = output[0].decode('utf-8')
        if val.strip() != '{}':
            lgr.error('Registry %s not reachable: %s' % (test_registry, output[0].decode('utf-8')))
            retval = False
    else:
        lgr.error('Registry %s not reachable: %s' % (test_registry, output[0].decode('utf-8')))
        retval = False
    return retval
    
def getTags(image, test_registry):
    cmd =   'curl --silent --header "Accept: application/vnd.docker.distribution.manifest.v2+json"  "http://%s/v2/%s/tags/list"' % (test_registry, image)
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].strip()) > 0:
        j = json.loads(output[0].decode('utf-8'))
        if 'tags' in j:
            return j['tags']
        else:
            return None
    else:
        return None

def getDigest(image, tag, test_registry):
    cmd =   'curl --silent --header "Accept: application/vnd.docker.distribution.manifest.v2+json"  "http://%s/v2/%s/manifests/%s"' % (test_registry, image, tag)
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].strip()) > 0:
        j = json.loads(output[0].decode('utf-8'))
        if 'config' in j:
            return j['config']['digest']
        else:
            return None
    else:
        return None

def getCreated(image, digest, test_registry):
    cmd = 'curl --silent --location "http://%s/v2/%s/blobs/%s"' % (test_registry, image, digest)
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].strip()) > 0:
        j = json.loads(output[0].decode('utf-8'))
        #print j['container_config']['User']
        version = None
        base = None
        if 'version' in j['container_config']['Labels']:
            version = j['container_config']['Labels']['version'] 
        if 'base' in j['container_config']['Labels']:
            base = j['container_config']['Labels']['base'] 
            if '/' in base:
                base = '%s/%s' % (test_registry, base.split('/')[1])
        return j['created'], j['container_config']['User'], version, base

#created, user, version, use_tag = inspectLocal('radius.radius.student', 'testregistry:5000', True)
#print '%s  user: %s version: %s use_tag %s' % (created, user, version, use_tag)
