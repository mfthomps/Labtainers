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
import LabtainerLogging
'''
Return creation date and user of a given image from a local registry, i.e.,
the test registry.
'''



def inspectLocal(image, lgr, test_registry):
    use_tag = 'latest'
    lgr.debug('inspectLocal image %s' % image)
    digest = getDigest(image, 'latest', test_registry)
    if digest is None:
        return None, None
    lgr.debug('inspectLocal digest %s' % digest)
    created, user = getCreated(image, digest, test_registry)
    #print('created %s  user %s' % (created, user))
    return created, user


    
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
        return j['created'], j['container_config']['User']

if __name__ == '__main__':
    logger = LabtainerLogging.LabtainerLogging("remotebase.log", 'none', "../../config/labtainer.config")
    inspectLocal(sys.argv[1], logger, 'testregistry:5000')
