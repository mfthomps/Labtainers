#!/usr/bin/env python
import sys
import os
import json
import logging
import argparse
import subprocess
import shlex
here = os.path.dirname(os.path.abspath(__file__))
student_dir = os.path.join(here,'../labtainer-student')
sys.path.append(os.path.join(student_dir, 'bin'))
sys.path.append(os.path.join(student_dir, 'lab_bin'))
import labutils
import LabtainerLogging
'''
Wraper functions for invoking Labtainer functions from GNS3
'''
def getImageMap(lab, logger):
    cmd = 'docker ps'
    ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) > 0:
        logger.error('No running containers: error returned %s, return false' % output[1])
        return None
    lookfor = ' %s_' % lab
    image_map = {}
    for line in output[0].decode('utf-8').splitlines():
        if lookfor in line:
            parts = line.split()
            image_map[parts[1]] = parts[0]
            logger.debug('getImageMap map %s to %s' % (parts[1], parts[0]))
    return image_map


def getLabFromImage(image_name):
    ''' strip off tag if present '''
    if ':' in image_name:
        image_name = image_name.rsplit(':', 1)[0]
    suffix = '-labtainer'
    if not image_name.endswith(suffix):
        print('%s not a labtainer' % image_name)
        return None, None
    index = len(suffix) * -1
    lab_box = image_name[:index]
    if lab_box.count('-') == 1:
        parts = lab_box.split('-')
    elif '_' in lab_box:
        parts = lab_box.rsplit('_', 1)
    else:
        print('could not parse lab/box from %s' % image_name)
        return None, None
    lab = parts[0]
    box = parts[1]
    return lab, box

def labtainerTerms(images, logger):
    labutils.logger = logger
    logger.debug('labtainerTerms %d images' % len(images))
    labname, box = getLabFromImage(images[0])
    here = os.path.dirname(os.path.abspath(__file__))
    gparent = os.path.dirname(os.path.dirname(here))
    lab_path = os.path.join(gparent, 'labs', labname)
    logger.debug('lab_path is %s' % lab_path)
    image_map = getImageMap(labname, logger)
    container_map = {}
    labtainer_config, start_config = labutils.GetBothConfigs(lab_path, logger)
    for name, container in start_config.containers.items():
        #print('name %s full %s' % (name, container.full_name))
        gimage = getGImage(labname, name)
        for image in image_map:
            if image.startswith(gimage):
                gcontainer = image_map[image]
                #print('got match %s cont %s' % (image, gcontainer))
                container_map[container.full_name] = gcontainer

    labutils.DoTerminals(start_config, lab_path, container_map = container_map)

def moreTerm(image, container_id, logger):
    labutils.logger = logger
    logger.debug('moreTerm mage %s' % image)
    labname, box = getLabFromImage(image)
    here = os.path.dirname(os.path.abspath(__file__))
    gparent = os.path.dirname(os.path.dirname(here))
    lab_path = os.path.join(gparent, 'labs', labname)
    logger.debug('lab_path is %s' % lab_path)

    labtainer_config, start_config = labutils.GetBothConfigs(lab_path, logger)
    for name, container in start_config.containers.items():
        #print('name %s full %s' % (name, container.full_name))
        gimage = getGImage(labname, name)
        if image.startswith(gimage):
            return labutils.DoMoreterm(lab_path, name, alt_name=container_id[:12])
    logger.error('moreTerm failed to find container for %s' % image)
    return False

def hasThumb(image_name, logger):
    labutils.logger = logger
    retval=True
    start_config, comp_name, labname, lab_path = getStartConfig(image_name, logger)
    running = labutils.GetContainerId(image_name)
    logger.debug('running is %s  ' % running)
    for name, container in start_config.containers.items():
        if name == comp_name:
            if container.thumb_volume is not None or container.thumb_command is not None:
                return True
            else:
                return False 

    return False 

def getTokenValue(line, token):
    parts = line.split()
    for p in parts:
        if '=' in p:
            tok, val = p.split('=')
            if tok.strip() == token:
                return val.strip()
    return None
        

def isThumbInserted(image_name, logger):
    ''' determine if a thumb drive for this component is inserted, baed on id info found in the usb create command '''
    # format of create command is:
    # idVendor=0x1d6b idProduct=0x0104
    labutils.logger = logger
    retval=False
    start_config, comp_name, labname, lab_path = getStartConfig(image_name, logger)
    for name, container in start_config.containers.items():
        if name == comp_name:
            logger.debug('is thumb inserted?')
            if container.thumb_command is not None:
                cmd_file = os.path.join(lab_path, container.thumb_command)
                if not os.path.isfile(cmd_file):
                    logger.error('Could not find file %s' % cmd_file)
                    return False
                vend_prod = None
                with open(cmd_file) as fh:
                    for line in fh:
                        vend = getTokenValue(line, 'idVendor') 
                        prod = getTokenValue(line, 'idProduct') 
                        if vend is not None and prod is not None:
                            ''' get rid of leading 0x '''
                            vend_prod = '%s:%s' % (vend[2:], prod[2:])
                if vend_prod is None:
                    logger.error('Did not find vendor and product in %s' % cmd_file)
                    return False
                cmd = ('lsusb')
                ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                output = ps.communicate()
                for line in output[0].decode('utf-8').splitlines():
                     parts = line.split()
                     this_vend_prod = parts[5]
                     logger.debug('compare %s to %s' % (vend_prod, this_vend_prod))
                     if vend_prod == this_vend_prod:
                         retval = True
                         break
    return retval

def thumbInsert(image_name, container_id, logger):
    ''' simulate insertion of usb drive by mounting a volume image using mount arguments
        found in the start.config THUMB_VOLUME argument '''
    labutils.logger = logger
    retval=True
    start_config, comp_name, labname, lab_path = getStartConfig(image_name, logger)
    running = labutils.GetContainerId(image_name)
    logger.debug('running is %s  ' % running)

    cwd = os.getcwd()
    os.chdir(student_dir)
    mount_cmd = None
    thumb_cmd = None
    for name, container in start_config.containers.items():
        if name == comp_name:
            if container.thumb_volume is not None:
                logger.debug('thumb volume: %s' % container.thumb_volume)
                logger.debug('thumb command: %s' % container.thumb_volume)
                mount_cmd = container.thumb_volume
                if container.thumb_command is not None:
                    thumb_cmd = 'sudo '+os.path.join(lab_path, container.thumb_command)
                    logger.debug('thumb_cmd %s' % thumb_cmd)
            else:
                logger.debug('The start.config has no THUMB_VOLUME entry for %s' % name)
                retval = False
            break

    if thumb_cmd is not None:
        ''' execute vm command, e.g., to attach usb device to a vm '''
        logger.debug('do thumb cmd')
        ps = subprocess.Popen(shlex.split(thumb_cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1].strip()) > 0:
            logger.error('ERROR from thumb cmd: %s' % output[1])
            retval = False
        else:
            for line in output[0].decode('utf-8').splitlines():
                logger.debug('thumb_cmd output: %s' % line)

    if mount_cmd is not None:
        running = labutils.GetContainerId(image_name)
        if running is not None:
            dock_cmd = 'docker exec %s script -q -c "sudo mount %s"' % (container_id, mount_cmd)
            logger.debug('mount cmd is %s' % dock_cmd)
            if not labutils.DockerCmd(dock_cmd):
                logger.error('docker exec failed')
                retval = False
    return retval

def thumbRemove(image_name, logger):        
    retval=True
    start_config, comp_name, labname, lab_path = getStartConfig(image_name, logger)
    cwd = os.getcwd()
    os.chdir(student_dir)
    mount_cmd = None
    thumb_cmd = None
    for name, container in start_config.containers.items():
        if name == comp_name:
            if container.thumb_stop is not None:
                cmd = 'sudo '+os.path.join(lab_path, container.thumb_stop)
                logger.debug('thumb_stop command %s' % cmd)
                ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                output = ps.communicate()
                if len(output[1].strip()) > 0:
                    logger.error('thumb stop failed %s\%s' % (container.thumb_stop, output[1]))
                    retval = False
                    break
    return retval

def gatherZips(zip_list, image, logger):
    labutils.logger = logger
    here = os.path.dirname(os.path.abspath(__file__))
    labname, name = getLabFromImage(image)
    parent = os.path.dirname(here)
    gparent = os.path.dirname(parent)
    lab_path = os.path.join(gparent, 'labs', labname)
    logger.debug('gatherZips lab_path is %s' % lab_path)
    labtainer_config, start_config = labutils.GetBothConfigs(lab_path, logger)
    labutils.GatherZips(zip_list, labtainer_config, start_config, labname, lab_path)

def getGImage(labname, name):
    return '%s_%s-labtainer' % (labname, name)

def labtainerStop(image, container_id, logger):
    labutils.logger = logger
    here = os.path.dirname(os.path.abspath(__file__))
    labname, name = getLabFromImage(image)
    parent = os.path.dirname(here)
    gparent = os.path.dirname(parent)
    lab_path = os.path.join(gparent, 'labs', labname)
    logger.debug('labtainerStop lab_path is %s' % lab_path)
    labtainer_config, start_config = labutils.GetBothConfigs(lab_path, logger)
    here = os.getcwd()
    student_dir = os.path.join(parent, 'labtainer-student')
    os.chdir(student_dir)
    zip_file_name = None
    for name, container in start_config.containers.items():
        logger.debug('name %s full %s' % (name, container.full_name))
        gimage = getGImage(labname, name)
        if image.startswith(gimage):

            labutils.GatherOtherArtifacts(lab_path, name, container_id, container.user, container.password, True)
            base_file_name, zip_file_name = labutils.CreateCopyChownZip(start_config, labtainer_config, name,
                             container.full_name, container.image_name, container.user, container.password, True, True, running_container=container_id)

            if container.thumb_stop is not None:
                cmd = 'sudo '+os.path.join(lab_path, container.thumb_stop)
                logger.debug('thumb_stop command %s' % cmd)
                ps = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                output = ps.communicate()
                if len(output[1].strip()) > 0:
                    logger.error('thumb stop failed %s\%s' % (container.thumb_stop, output[1]))
                    return None
            
    os.chdir(here)
    return zip_file_name

def getStartConfig(image_name, logger):
    here = os.path.dirname(os.path.abspath(__file__))
    labname, comp_name = getLabFromImage(image_name)
    if labname is None:
        log.error('no labtainer labname found in image %s' % image_name)
        return None, None, None, None
    parent = os.path.dirname(here)
    gparent = os.path.dirname(parent)
    lab_path = os.path.join(gparent, 'labs', labname)
    logger.debug('paremterizeOne lab_path is %s' % lab_path)
    labtainer_config, start_config = labutils.GetBothConfigs(lab_path, logger)
    return start_config, comp_name, labname, lab_path

def parameterizeOne(image_name, logger):
    labutils.logger = logger
    start_config, comp_name, labname, lab_path = getStartConfig(image_name, logger)
    running = labutils.GetContainerId(image_name)
    logger.debug('running is %s  ' % running)
    email_addr = labutils.getLastEmail()
    if email_addr is None:
        logger.error('Missing labtainer email address')
        ''' TBD dialog?  Tell user how to add it '''
        return
   
    cwd = os.getcwd()
    logger.debug('parameterizeOne in %s need to be in %s' % (cwd, student_dir))
    os.chdir(student_dir)
    for name, container in start_config.containers.items():
        if name == comp_name:
                logger.debug('found match container name %s' % name)
                labutils.ParamForStudent(start_config.lab_master_seed, container.full_name, container.user, container.password,
                                labname, email_addr, lab_path, name, None, running_container = running)
                os.chdir(cwd)
                if container.kick_me is not None:
                    ''' gns3 cloud interfaces that share NICs get hung up after the first container shutdown.
                        For magical reasons, pinging the container from the VM wakes it up. '''
                    for subnet in container.container_nets:
                        if container.kick_me in container.container_nets:
                            ip = container.container_nets[container.kick_me]
                            cmd = 'ping -c 1 %s' % ip
                            os.system(cmd)
                            logger.info('kicked with %s' % cmd)
                        else: 
                            logger.debug('kickme %s not found for %s' % (container.kick_me, name))
                break
    os.chdir(cwd)

def extraHosts(image_name, logger):
    ''' gns3 style extra host processing '''
    retval = ''
    labutils.logger = logger

    start_config, comp_name, labname, lab_path = getStartConfig(image_name, logger)
    for name, container in start_config.containers.items():
        if name == comp_name:
            logger.debug('extraHosts found match container name %s' % name)
            for item in container.add_hosts:
                if ':' not in item:
                   if item in start_config.lan_hosts:
                       for entry in start_config.lan_hosts[item]:
                           host, ip = entry.split(':')
                           retval = retval + '%s\t%s\n' % (host.strip(), ip.strip())
                   else:
                       logger.error('ADD-HOST entry in start.config missing colon: %s' % item)
                       logger.error('sytax: ADD-HOST <host>:<ip>')
                       return retval
                else:
                   host, ip = item.split(':')
                   retval = retval + '%s\t%s\n' % (ip.strip(), host.strip())
            break 
    return retval

def isHidden(image_name, logger):
    labutils.logger = logger
    retval = False
    start_config, comp_name, labname, lab_path = getStartConfig(image_name, logger)
    for name, container in start_config.containers.items():
        if name == comp_name:
            if container.hide.lower() == 'yes':
                retval = True
    return retval

if __name__ == '__main__':
    ''' only for testing '''
    home = os.getenv("HOME")
    gns3_path = os.path.join(home, 'GNS3', 'projects')
    logger = LabtainerLogging.LabtainerLogging("test.log", 'eh', "../../config/labtainer.config")
    parser = argparse.ArgumentParser(description='Generate gns3 network interfaces file.')
    parser.add_argument('labname', help='Name of labtainers lab')
    parser.add_argument('gns3_proj', help='Name of gns3 project')
    parser.add_argument('fun', help='Name of function to test') 
    args = parser.parse_args()
    
    gns3_proj = os.path.join(gns3_path, args.gns3_proj, args.gns3_proj+'.gns3')
    if args.fun == 'term':
        images = {}
        with open(gns3_proj) as fh:
            gns3_json = json.load(fh)
            for node in gns3_json['topology']['nodes']:
                image = node['properties']['image']
                images[image] = node['properties']['container_id']
        labtainerTerms(images, logger)
    elif args.fun == 'stop':
        image = None
        zip_file_list = []
        with open(gns3_proj) as fh:
            gns3_json = json.load(fh)
            for node in gns3_json['topology']['nodes']:
                image = node['properties']['image']
                if 'labtainer' in image:
                    labname, box = getLabFromImage(image)
                    container_id = node['properties']['container_id']
                    zip_file = labtainerStop(image, container_id, logger)
                    if zip_file is None:
                        logger.error('zipfile is none for image %s  is it running?' % image)
                        exit(1)
                    zip_file_list.append(zip_file)
        if len(zip_file_list) > 0:
            gatherZips(zip_file_list, image, logger)
        else:
            print('No zipfiles found, are containers running?')
    elif args.fun == 'param':
        image = None
        with open(gns3_proj) as fh:
            gns3_json = json.load(fh)
            for node in gns3_json['topology']['nodes']:
                image = node['properties']['image']
                if 'labtainer' in image:
                    parameterizeOne(image, logger)
