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
                return
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
