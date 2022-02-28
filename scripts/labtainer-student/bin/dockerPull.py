#!/usr/bin/env python3
import docker
import json
import sys
def moveUp(rows):
    cmd = "\033[%dF" % rows
    sys.stdout.write(cmd)
def moveDown(rows):
    cmd = "\033[%dE" % rows
    sys.stdout.write(cmd)
def clearLine():
    cmd = "\033[2K"
    sys.stdout.write(cmd)
def hide():
    cmd = "\033[?25l"
    sys.stdout.write(cmd)
def show():
    cmd = "\033[?25h"
    sys.stdout.write(cmd)
def log(s, logger):
    if logger is not None:
        logger.debug(s)
 
def pull(full_image_name, logger=None):
    client = docker.from_env()
    #image = client.images.pull(full)
    #print(image.id)
    layers = []
    old_index = 0
    try:
        pull_result = client.api.pull(full_image_name, stream=True, decode=True)
    except:
        print('Failed Docker pull of %s, network problem or image does not exist.' % full_image_name)
        log(('Failed Docker pull of %s, network problem or image does not exist.' % full_image_name),logger)
        return False
    for line in pull_result:
        if 'status' not in line:
            continue
        status = line['status']
        if status.startswith('Digest:') or status.startswith('Status:'):
            sys.stdout.write('%s\n' % status)
            continue
        if status.startswith('Already exists'):
            continue
        #elif status.startswith('Pulling'):
        #    continue
        #elif status.startswith('Wait'):
        #    continue
        index = 0
        thisid = line['id']
        i = 0
        if thisid in layers:
            index = layers.index(thisid)+1
        # move the cursor
        if index > 0:
            diff = index - old_index
            if diff > 1:
                down = diff - 1
                moveDown(down)
            elif diff < 1:
                up = diff*-1 + 1
                moveUp(up)
            old_index = index 
        else:
            layers.append(thisid)
            diff = len(layers) - old_index
            if diff > 1:
                moveDown(diff)
            old_index = len(layers)
        clearLine()
        if status == 'Pull complete':
            sys.stdout.write('%s: %s\n' % (thisid, status))
        elif 'progress' in line:
            progress = line['progress']
            sys.stdout.write('%s: %s %s\n' % (thisid, status, progress))
        else:
            sys.stdout.write('%s: %s\n' % (thisid, status))
    
        #elif status.startswith('Pulling'):
        #    sys.stdout.write(status+'\n')
        #elif status.startswith('Waiting'):
        #    sys.stdout.write(status+'\n')
    show()
    return True
