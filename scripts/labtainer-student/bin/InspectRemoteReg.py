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
Return creation date and user of a given image from the Docker Hub
without pulling the image.
'''
def inspectRemote(image):
    token = getToken(image)
    if token is None or len(token.strip()) == 0:
        return None, None, None
    digest = getDigest(token, image, 'latest')
    if digest is None:
        return None, None, None
    created, user, version = getCreated(token, image, digest)
    return created, user, version

def getToken(image):
    cmd = 'curl --silent "https://auth.docker.io/token?scope=repository:%s:pull&service=registry.docker.io"' % (image) 
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    
    if len(output[0].strip()) > 0:
        j = json.loads(output[0])
        return j['token']
    else:
        return None

def getDigest(token, image, tag):
    cmd = 'curl --silent --header "Accept: application/vnd.docker.distribution.manifest.v2+json" --header "Authorization: Bearer %s" "https://registry-1.docker.io/v2/%s/manifests/%s"' % (token, image, tag) 
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].strip()) > 0:
        j = json.loads(output[0])
        if 'config' in j:
            return j['config']['digest']
        else:
            ''' assume not found error? '''
            return None
    else:
        return None

def getCreated(token, image, digest):
    cmd = 'curl --silent --location --header "Authorization: Bearer %s" "https://registry-1.docker.io/v2/%s/blobs/%s"' % (token, image, digest)
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[0].strip()) > 0:
        j = json.loads(output[0])
        return j['created'], j['container_config']['User'], j['container_config']['Labels']['version']
    else:
        return None, None, None

