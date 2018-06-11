#!/usr/bin/env python
'''
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
'''
import os
import sys
import json
import subprocess
'''
Return creation date and user of a given image from a local registry, i.e.,
the test registry.
'''

def inspectLocal(image, test_registry):
    digest = getDigest(image, 'latest', test_registry)
    if digest is None:
        return None, None, None
    created, user, version = getCreated(image, digest, test_registry)
    return created, user, version
    
def getDigest(image, tag, test_registry):
    cmd =   'curl --silent --header "Accept: application/vnd.docker.distribution.manifest.v2+json"  "http://%s/v2/%s/manifests/%s"' % (test_registry, image, tag)
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].strip()) > 0:
        j = json.loads(output[0])
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
        j = json.loads(output[0])
        #print j['container_config']['User']
        version = None
        if 'version' in j['container_config']['Labels']:
            verstion = j['container_config']['Labels']['version'] 
        return j['created'], j['container_config']['User'], version

#created, user = inspectLocal('onewayhash.onewayhash.student', 'testregistry:5000')
#print '%s  user: %s' % (created, user)
