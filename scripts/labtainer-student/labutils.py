import filecmp
import glob
import json
import md5
import os
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

'''
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
'''

LABS_ROOT = os.path.abspath("../../labs/")
LABTAINER_CONFIG = os.path.abspath("../../config/labtainer.config")

# Error code returned by docker inspect
SUCCESS=0
FAILURE=1

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def isalphadashscore(name):
    # check name - alphanumeric,dash,underscore
    return re.match(r'^[a-zA-Z0-9_-]*$', name)

# get docker0 IP address
def getDocker0IPAddr():
    return get_ip_address('docker0')

# Parameterize my_container_name container
def ParameterizeMyContainer(mycontainer_name, container_user, lab_instance_seed, user_email, labname):
    retval = True
    #print "About to call parameterize.sh with LAB_INSTANCE_SEED = (%s)" % lab_instance_seed
    command = 'docker exec -it %s script -q -c "/home/%s/.local/bin/parameterize.sh %s %s %s %s" /dev/null' % (mycontainer_name, container_user, lab_instance_seed, user_email, labname, mycontainer_name)
    ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1]) > 0:
        print('ERROR: ParaemterizeMyContainer %s' % output[1])
        print('command was %s' % command)
        retval = False
    return retval

# Start my_container_name container
def StartMyContainer(mycontainer_name):
    retval = True
    command = "docker start %s" % mycontainer_name
    ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1]) > 0:
        print('ERROR: ParaemterizeMyContainer %s' % str(output))
        print('command was %s' % command)
        retval = False
    return retval

# Check to see if my_container_name container has been created or not
def IsContainerCreated(mycontainer_name):
    retval = True
    command = "docker inspect -f {{.Created}} --type container %s 2> /dev/null" % mycontainer_name
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    if result == FAILURE:
       retval = False
    #print "Result of subprocess.call IsContainerCreated is %s" % result
    return retval

def ConnectNetworkToContainer(mycontainer_name, mysubnet_name, mysubnet_ip):
    #print "Connecting more network subnet to container %s" % mycontainer_name
    command = "docker network connect --ip=%s %s %s 2> /dev/null" % (mysubnet_ip, mysubnet_name, mycontainer_name)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call ConnectNetworkToContainer is %s" % result
    return result

def DisconnectNetworkFromContainer(mycontainer_name, mysubnet_name):
    #print "Disconnecting more network subnet to container %s" % mycontainer_name
    command = "docker network disconnect %s %s 2> /dev/null" % (mysubnet_name, mycontainer_name)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call DisconnectNetworkFromContainer is %s" % result
    return result

def CreateSingleContainer(mycontainer_name, mycontainer_image_name, hostname, mysubnet_name=None, mysubnet_ip=None):
    #print "Create Single Container"
    docker0_IPAddr = getDocker0IPAddr()
    #print "getDockerIPAddr result (%s)" % docker0_IPAddr
    if mysubnet_name:
        createsinglecommand = "docker create -t --network=%s --ip=%s --privileged --add-host my_host:%s --name=%s --hostname %s %s bash" % (mysubnet_name, mysubnet_ip, docker0_IPAddr, mycontainer_name, hostname, mycontainer_image_name)
    else:
        createsinglecommand = "docker create -t --privileged --add-host my_host:%s --name=%s --hostname %s %s bash" % (docker0_IPAddr, 
           mycontainer_name, hostname, mycontainer_image_name)
    #print "Command to execute is (%s)" % createsinglecommand
    result = subprocess.call(createsinglecommand, shell=True)
    #print "Result of subprocess.call CreateSingleContainer is %s" % result
    return result


# Create SUBNETS
def CreateSubnets(subnets):
    #for (subnet_name, subnet_network_mask) in networklist.iteritems():
    for subnet_name in subnets:
        subnet_network_mask = subnets[subnet_name].mask
        #print "subnet_name is %s" % subnet_name
        #print "subnet_network_mask is %s" % subnet_network_mask

        command = "docker network inspect %s > /dev/null" % subnet_name
        #print "Command to execute is (%s)" % command
        inspect_result = subprocess.call(command, shell=True)
        #print "Result of subprocess.call CreateSubnets docker network inspect is %s" % inspect_result
        if inspect_result == FAILURE:
            # Fail means does not exist - then we can create
            if subnets[subnet_name].gateway != None:
                #print subnets[subnet_name].gateway
                subnet_gateway = subnets[subnet_name].gateway
                command = "docker network create -d bridge --gateway=%s --subnet %s %s" % (subnet_gateway, subnet_network_mask, subnet_name)
            else:
                command = "docker network create -d bridge --subnet %s %s" % (subnet_network_mask, subnet_name)
            #print "Command to execute is (%s)" % command
            #create_result = subprocess.call(command, shell=True)
            ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = ps.communicate()
            #print "Result of subprocess.call CreateSubnets docker network create is %s" % create_result
            if len(output[1]) > 0:
                sys.stderr.write("ERROR: Failed to create %s subnet at %s, %s\n" % (subnet_name, subnet_network_mask, output[1]))
                sys.stderr.write("command was %s\n" % command)
                sys.exit(1)
        else:
            print "Already exists! Not creating %s subnet at %s!\n" % (subnet_name, subnet_network_mask)

def RemoveSubnets(subnets):
    for subnet_name in subnets:
        command = "docker network rm %s" % subnet_name
        remove_result = subprocess.call(command, shell=True)

EMAIL_TMP='./.tmp/email.txt' 
def getLastEmail():
    retval = None
    if os.path.isfile(EMAIL_TMP):
        with open(EMAIL_TMP) as fh:
            retval = fh.read()
    return retval

def putLastEmail(email):
    try:
        os.mkdir('./.tmp')
    except:
        pass
    with open(EMAIL_TMP, 'w') as fh:
            fh.write(email)

def ParamForStudent(lab_master_seed, mycontainer_name, container_user, labname, student_email):
    if student_email is not None:
        user_email = student_email
    else:
        done = False
        while not done and student_email is None:
            done = True
            # Prompt user for e-mail address
            eprompt = 'Please enter your e-mail address: '
            prev_email = getLastEmail()
            if prev_email is not None:
                eprompt = eprompt+" [%s]" % prev_email
            user_email = raw_input(eprompt)
            if len(user_email.strip()) == 0:
                if prev_email is None:
                    done = False
                else:
                    user_email = prev_email
            else:
                putLastEmail(user_email)
    
    # Create hash using LAB_MASTER_SEED concatenated with user's e-mail
    # LAB_MASTER_SEED is per laboratory - specified in start.config
    string_to_be_hashed = '%s:%s' % (lab_master_seed, user_email)
    mymd5 = md5.new()
    mymd5.update(string_to_be_hashed)
    mymd5_hex_string = mymd5.hexdigest()
    #print mymd5_hex_string

    if not ParameterizeMyContainer(mycontainer_name, container_user, mymd5_hex_string,
                                                          user_email, labname):
        sys.stderr.write("ERROR: Failed to parameterize lab container %s!\n" % mycontainer_name)
        sys.exit(1)
    return user_email

# Copy Students' Artifacts from host to instructor's lab container
def CopyStudentArtifacts(labtainer_config, mycontainer_name, labname, container_user, is_regress_test):
    # Set the lab name 
    command = 'docker exec -it %s script -q -c "echo %s > /home/%s/.local/.labname" /dev/null' % (mycontainer_name, labname, container_user)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call CopyStudentArtifacts set labname is %s" % result
    if result == FAILURE:
        sys.stderr.write("ERROR: Failed to set labname in container %s!\n" % mycontainer_name)
        sys.exit(1)

    username = getpass.getuser()
    if is_regress_test:
        xfer_dir = labtainer_config.testsets_root
        zip_filelist = glob.glob('%s/*.zip' % xfer_dir)
    else:
        xfer_dir = labtainer_config.host_home_xfer
        zip_filelist = glob.glob('/home/%s/%s/*.zip' % (username, xfer_dir))
    #print "filenames is (%s)" % zip_filelist
    # Copy zip files from 'Shared' folder to 'home/$CONTAINER_USER'
    for fname in zip_filelist:
        #print "name is %s" % fname
        base_fname = os.path.basename(fname)
        # Copy zip file and chown it
        command = 'docker cp %s %s:/home/%s/' % (fname, mycontainer_name, container_user)
        #print "Command to execute is (%s)" % command
        result = subprocess.call(command, shell=True)
        #print "Result of subprocess.call CopyStudentArtifacts copy zipfile (%s) is %s" % (fname, result)
        if result == FAILURE:
            sys.stderr.write("ERROR: Failed to set labname in container %s!\n" % mycontainer_name)
            sys.exit(1)
        command = 'docker exec -it %s sudo chown %s:%s /home/%s/%s' % (mycontainer_name, container_user, container_user, container_user, base_fname)
        #print "Command to execute is (%s)" % command
        result = subprocess.call(command, shell=True)
        #print "Result of subprocess.call CopyStudentArtifacts copy zipfile (%s) is %s" % (fname, result)
        if result == FAILURE:
            sys.stderr.write("ERROR: Failed to set labname in container %s!\n" % mycontainer_name)
            sys.exit(1)

def DoStart(start_config, labtainer_config, labname, role, is_regress_test):
    lab_master_seed = start_config.lab_master_seed
    #print "Do: START Multiple Containers and/or multi-home networking"

    # Create SUBNETS
    CreateSubnets(start_config.subnets)
    student_email = None
    for name, container in start_config.containers.items():
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        container_user         = container.user
        container_hostname         = container.hostname

        haveContainer = IsContainerCreated(mycontainer_name)
        #print "DoStart IsContainerCreated result (%s)" % haveContainer

        # Set need_seeds=False first
        need_seeds=False

        # IsContainerCreated return False if container does not exists
        if not haveContainer:
            # Container does not exist, create the container
            # Use CreateSingleContainer()
            if len(container.container_nets) == 0:
                containerCreated = CreateSingleContainer(mycontainer_name, mycontainer_image_name, container_hostname)
            else:
                mysubnet_name, mysubnet_ip = container.container_nets.popitem()
                containerCreated = CreateSingleContainer(mycontainer_name, mycontainer_image_name, container_hostname,
                                                         mysubnet_name, mysubnet_ip)
                
            #print "CreateSingleContainer result (%s)" % containerCreated
            # Give the container some time -- just in case
            time.sleep(3)
            # If we just create it, then set need_seeds=True
            need_seeds=True

        # Check again - 
        haveContainer = IsContainerCreated(mycontainer_name)
        #print "IsContainerCreated result (%s)" % haveContainer

        # IsContainerCreated returned False if container does not exists
        if not haveContainer:
            sys.stderr.write("ERROR: DoStart Container %s still not created!\n" % mycontainer_name)
            sys.exit(1)
        else:
            for mysubnet_name, mysubnet_ip in container.container_nets.items():
                connectNetworkResult = ConnectNetworkToContainer(mycontainer_name, mysubnet_name, mysubnet_ip)

            # Start the container
            if not StartMyContainer(mycontainer_name):
                sys.stderr.write("ERROR: DoStart Container %s failed to start!\n" % mycontainer_name)
                sys.exit(1)

        if role == 'instructor':
            '''
            Copy students' artifacts only to the container where 'Instructor.py' supposed
            to be run - where <labname>.grades.txt will later reside also (i.e., don't copy to all containers)
            Copy to container named start_config.grade_container
            '''
            if mycontainer_name == start_config.grade_container:
                copy_result = CopyStudentArtifacts(labtainer_config, mycontainer_name, labname, container_user, is_regress_test)
                if copy_result == FAILURE:
                    sys.stderr.write("ERROR: DoStart Failed to copy students' artifacts to container %s!\n" % mycontainer_name)
                    sys.exit(1)
        # If the container is just created, prompt user's e-mail
        # then parameterize the container
        elif need_seeds and role == 'student':
            student_email = ParamForStudent(lab_master_seed, mycontainer_name, container_user, labname, student_email)
    
    # Reach here - Everything is OK - spawn terminal for each container based on num_terminal
    for container in start_config.containers.values():
        num_terminal = container.terminals
        mycontainer_name = container.full_name
        #print "Number of terminal is %d" % num_terminal
        # If the number of terminal is zero -- do not spawn
        if num_terminal != 0:
            for x in range(num_terminal):
                spawn_command = "gnome-terminal -x docker exec -it %s bash -l &" % mycontainer_name
                os.system(spawn_command)

    return 0


# Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
def CreateHostHomeXfer(host_xfer_dir):
    # remove trailing '/'
    host_xfer_dir = host_xfer_dir.rstrip('/')
    #print "host_home_xfer directory (%s)" % host_xfer_dir
    if os.path.exists(host_xfer_dir):
        # exists but is not a directory
        if not os.path.isdir(host_xfer_dir):
            # remove file then create directory
            os.remove(host_xfer_dir)
            os.makedirs(host_xfer_dir)
        #else:
        #    print "host_home_xfer directory (%s) exists" % host_xfer_dir
    else:
        # does not exists, create directory
        os.makedirs(host_xfer_dir)

# CopyChownGradesFile
def CopyChownGradesFile(mycwd, start_config, labtainer_config, container_name, container_image, container_user):
    host_home_xfer = labtainer_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed
    labname = start_config.labname

    username = getpass.getuser()

    # Copy <labname>.grades.txt file
    grade_filename = '/home/%s/%s.grades.txt' % (container_user, labname)
    command = "docker cp %s:%s /home/%s/%s" % (container_name, grade_filename, username, host_home_xfer)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CopyChownGradesFile: Result of subprocess.Popen exec cp %s.grades.txt file is %s" % (labname, result)
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("WARNING: CopyChownGradesFile Container %s fail on executing cp %s.grades.txt file!\n" % (container_name, labname))
        #sys.exit(1)
        return

    # Change <labname>.grades.txt ownership to defined user $USER
    command = "sudo chown %s:%s /home/%s/%s/%s.grades.txt" % (username, username, username, host_home_xfer, labname)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CopyChownGradesFile: Result of subprocess.Popen exec chown %s.grades.txt file is %s" % (labname, result)
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CopyChownGradesFile Container %s fail on executing chown %s.grades.txt file!\n" % (container_name, labname))
        sys.exit(1)

    # Copy <labname>.grades.json file
    gradejson_filename = '/home/%s/%s.grades.json' % (container_user, labname)
    command = "docker cp %s:%s /home/%s/%s" % (container_name, gradejson_filename, username, host_home_xfer)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CopyChownGradesFile: Result of subprocess.Popen exec cp %s.grades.json file is %s" % (labname, result)
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("WARNING: CopyChownGradesFile Container %s fail on executing cp %s.grades.json file!\n" % (container_name, labname))
        #sys.exit(1)
        return

    # Change <labname>.grades.json ownership to defined user $USER
    command = "sudo chown %s:%s /home/%s/%s/%s.grades.json" % (username, username, username, host_home_xfer, labname)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CopyChownGradesFile: Result of subprocess.Popen exec chown %s.grades.json file is %s" % (labname, result)
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CopyChownGradesFile Container %s fail on executing chown %s.grades.json file!\n" % (container_name, labname))
        sys.exit(1)

def StartLab(labname, role, is_regress_test):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
   
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, role)
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(LABTAINER_CONFIG, labname)
    host_home_xfer = labtainer_config.host_home_xfer

    # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
    host_xfer_dir = '%s/%s' % (myhomedir, host_home_xfer)
    CreateHostHomeXfer(host_xfer_dir)

    DoStart(start_config, labtainer_config, labname, role, is_regress_test)

def FileModLater(ts, fname):
    ''' is the given file later than the timestamp (which is in UTC)? '''
    df_time = os.path.getmtime(fname)
    #print('df ts %s' % df_time)

    df_string = datetime.datetime.fromtimestamp(df_time)
    #print('df_local time is %s' % df_string)

    df_utc_string = str(datetime.datetime.utcfromtimestamp(df_time))
    parts = df_utc_string.split('.')
    df_ts = time.mktime(time.strptime(parts[0], "%Y-%m-%d %H:%M:%S"))

    #print('df_utc time is %s' % df_utc_string)
    #print('df_utc ts is %s given ts is %s' % (df_ts, ts))
    if df_ts > ts:
        return True
    else:
        return False

def CheckBuild(labname, image_name, container_name, name, role):
    '''
    Determine if a container image needs to be rebuilt.
    '''
    retval = False
    #print('check build for container %s image %s' % (container_name, image_name))
    cmd = "docker inspect -f '{{.Created}}' --type image %s" % image_name
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result = child.stdout.read().strip()
    if 'Error:' in result or len(result.strip()) == 0:
        return True
    #print('result is %s' % result)
    parts = result.strip().split('.')
    time_string = parts[0]
    #print('image time string %s' % time_string)

    ''' ts is the timestamp of the image '''
    ts = time.mktime(time.strptime(time_string, "%Y-%m-%dT%H:%M:%S"))
    #print('image ts %s' % ts)


    lab_path = os.path.join(LABS_ROOT,labname)
    df_name = 'Dockerfile.%s' % container_name
    df = os.path.join(lab_path, 'dockerfiles', df_name)
    if FileModLater(ts, df):
        print('dockerfile changed, will build')
        retval = True
    else:
        container_dir = os.path.join(lab_path, name)
        #print('container dir %s' % container_dir)
        if FileModLater(ts, container_dir):
           print('%s is later, will build' % container_dir)
           retval = True
        else:
            for folder, subs, files in os.walk(container_dir):
                for f in files:
                   f_path = os.path.join(folder, f)
                   if FileModLater(ts, f_path):
                       print('%s is later, will build' % f_path)
                       retval = True
                       break

    if not retval:
        all_bin = './bin' 
        all_bin_files = os.listdir(all_bin)
        for f in all_bin_files:
            f_path = os.path.join(all_bin, f)
            if FileModLater(ts, f_path):
               print('%s is later, will build' % f_path)
               retval = True
               break

    if not retval and role == 'instructor':
        inst_cfg = os.path.join(lab_path,'instr_config')
        inst_cfg_files = os.listdir(inst_cfg)
        for f in inst_cfg_files:
            f_path = os.path.join(inst_cfg, f)
            if FileModLater(ts, f_path):
               print('%s is later, will build' % f_path)
               retval = True
               break
        print('is instructor')
        if not retval:  
            inst_bin = './bin'
            inst_bin_files = os.listdir(inst_bin)
            for f in inst_bin_files:
                f_path = os.path.join(inst_bin, f)
                if FileModLater(ts, f_path):
                   print('%s is later, will build' % f_path)
                   retval = True
                   break
    return retval

def dumb():
    pass
    '''
    '''
def RedoLab(labname, role, is_regress_test):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, role)
    StopLab(labname, role)
    build_student = './buildImage.sh'
    build_instructor = './buildInstructorImage.sh'
    fixresolve='../../setup_scripts/fixresolv.sh'
    didfix = False
    for name, container in start_config.containers.items():
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        cmd = 'docker rm %s' % mycontainer_name
        os.system(cmd)
        #print('did %s' % cmd)
        if CheckBuild(labname, mycontainer_image_name, mycontainer_name, name, role):
            if os.path.isfile(fixresolve) and not didfix:
                ''' DNS name resolution from containers (while being built) fails when behind NAT? '''
                os.system(fixresolve)
                didfix=True
            if os.path.isfile(build_student):
                cmd = '%s %s %s' % (build_student, labname, name)
            elif os.path.isfile(build_instructor):
                cmd = '%s %s %s' % (build_instructor, labname, name)
            else:
                sys.stderr.write("ERROR: RedoLab, no image rebuild script\n")
                exit(1)
                 
            if os.system(cmd) != 0:
                sys.stderr.write("ERROR: build of image failed\n")
                exit(1)
    StartLab(labname, role, is_regress_test)

def GatherOtherArtifacts(labname, name, container_name, container_user):
    '''
    Parse the results.config file looking for files named by absolute paths,
    and copy those into the .local/result directory, maintaining the original
    directory structure, e.g., .local/result/var/log/foo.log
    '''
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"instr_config") 
    results_config_path = os.path.join(config_path,"results.config")
    did_file = []
    with open (results_config_path) as fh:
        for line in fh:
            ''' container:filename is between "=" and first " : " '''
            line = line.strip()
            if line.startswith('#') or len(line) == 0:
                continue
            if '=' not in line:
                print('no = in line %s' % line)
                continue
            after_equals = line.split('=', 1)[1]
            fname = after_equals.split(' : ')[0]
            is_mine = False
            if ':' in fname:
                f_container, fname = fname.split(':')
                #print('f_container <%s> container_name %s' % (f_container, name))
                if f_container.strip() == name:
                    is_mine = True 
                fname = fname.strip()
            else: 
                is_mine = True
            if is_mine:
                #print(' is mine %s' % fname )
                if fname.startswith('/') and fname not in did_file:
                    ''' copy from abs path to ~/.local/result ''' 
               
                    command='docker exec -it %s sudo cp --parents %s /home/%s/.local/result' % (container_name, fname, container_user)
                    #print command
                    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    error = child.stderr.read().strip()
                    if len(error) > 0:
                        print('GatherOtherArtifacts, ERROR: %s' % error)
                        print('command was %s' % command)
                    did_file.append(fname)
                    command='docker exec -it %s sudo chmod a+r -R /home/%s/.local/result' % (container_name, container_user)
                    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    error = child.stderr.read().strip()
                    if len(error) > 0:
                        print('GatherOtherArtifacts, chmod ERROR: %s' % error)
                        print('command was %s' % command)
                        

# RunInstructorCreateGradeFile
def RunInstructorCreateGradeFile(container_name):
    # Run 'instructor.py' - This will create '<labname>.grades.txt' 
#   print "About to call instructor.py"
    bash_command = "'cd ; . .profile ; instructor.py'"
    command = 'docker exec -it %s script -q -c "/bin/bash -c %s" /dev/null' % (container_name, bash_command)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
#   print "RunInstructorCreateGradeFile: Result of subprocess.call exec instructor.py is %s" % result
    if result == FAILURE:
        sys.stderr.write("ERROR: RunInstructorCreateGradeFile Container %s fail on executing instructor.py!\n" % container_name)
        sys.exit(1)


def RegressTest(labname, role):
    username = getpass.getuser()
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, role)

    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(LABTAINER_CONFIG, labname)
    regresstest_lab_path = labtainer_config.testsets_root
    host_home_xfer = labtainer_config.host_home_xfer
    print "Host Xfer directory for labname %s is %s" % (labname, host_home_xfer)
    print "Regression Test path for labname %s is %s" % (labname, regresstest_lab_path)

    GradesGold = "%s/%s.grades.txt" % (regresstest_lab_path, labname)
    Grades = "/home/%s/%s/%s.grades.txt" % (username, host_home_xfer, labname)
    #print "GradesGold is %s - Grades is %s" % (GradesGold, Grades)

    RedoLab(labname, role, True)
    RunInstructorCreateGradeFile(start_config.grade_container)
    StopLab(labname, role)

    CompareResult = filecmp.cmp(GradesGold, Grades)
    return CompareResult


# CreateCopyChownZip
def CreateCopyChownZip(mycwd, start_config, labtainer_config, container_name, container_image, container_user):
    #TODO: FIX
    host_home_xfer  = labtainer_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed

    # Run 'Student.py' - This will create zip file of the result
#   print "About to call Student.py"
    bash_command = "'cd ; . .profile ; Student.py'"
#   bash_command = "'cd ; . .bash_profile ; Student.py'"
    command = 'docker exec -it %s script -q -c "/bin/bash -c %s" /dev/null' % (container_name, bash_command)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
#   print "CreateCopyChownZip: Result of subprocess.call exec Student.py is %s" % result
    if result == FAILURE:
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing Student.py!\n" % container_name)
        sys.exit(1)

    username = getpass.getuser()
    command='docker exec -it %s cat /home/%s/.local/zip.flist' % (container_name, container_user)
    #print "Command to execute is (%s)" % command
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    orig_zipfilenameext = child.stdout.read().strip()
#   print "CreateCopyChownZip: Result of subprocess.Popen exec cat zip.flist is %s" % orig_zipfilenameext
    if orig_zipfilenameext == None:
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing cat zip.flist!\n" % container_name)
        sys.exit(1)

    # The zip filename created by Student.py has the format of e-mail.labname.zip
    orig_zipfilename, orig_zipext = os.path.splitext(orig_zipfilenameext)
    baseZipFilename = os.path.basename(orig_zipfilename)
    #NOTE: Use the '=' to separate e-mail+labname from the container_name
    DestZipFilename = '%s=%s.zip' % (baseZipFilename, container_name)
    command = "docker cp %s:%s /home/%s/%s/%s" % (container_name, orig_zipfilenameext, username, host_home_xfer, DestZipFilename)
#   print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CreateCopyChownZip: Result of subprocess.Popen exec cp zip file is %s" % result
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing cp zip file!\n" % container_name)
        sys.exit(1)

    # Change ownership to defined user $USER
    command = "sudo chown %s:%s /home/%s/%s/*.zip" % (username, username, username, host_home_xfer)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CreateCopyChownZip: Result of subprocess.Popen exec chown zip file is %s" % result
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing chown zip file!\n" % container_name)
        sys.exit(1)

    currentContainerZipFilename = "/home/%s/%s/%s" % (username, host_home_xfer, DestZipFilename)
    return baseZipFilename, currentContainerZipFilename


# Stop my_container_name container
def StopMyContainer(mycwd, start_config, container_name):
    command = "docker stop %s 2> /dev/null" % container_name
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call StopMyContainer stop is %s" % result
    return result

def IsContainerRunning(mycontainer_name):
    try:
        s = subprocess.check_output('docker ps', shell=True)
    except:
        return False
    if mycontainer_name in s:
        return True
    else:
        return False 


def DoStop(start_config, labtainer_config, mycwd, labname, role):
    retval = True
    host_home_xfer  = labtainer_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed
    #print "Do: STOP Multiple Containers and/or multi-home networking"

    ZipFileList = []
    username = getpass.getuser()

    baseZipFilename = ""
    for name, container in start_config.containers.items():
        mycontainer_name  = container.full_name
        container_user    = container.user
        mycontainer_image = container.image_name
        haveContainer     = IsContainerCreated(mycontainer_name)
        #print "IsContainerCreated result (%s)" % haveContainer

        # IsContainerCreated returned FAILURE if container does not exists
        # error: can't stop non-existent container
        if not haveContainer:
            sys.stderr.write("ERROR: DoStopMultiple Container %s does not exist!\n" % mycontainer_name)
            retval = False
        elif not IsContainerRunning(mycontainer_name):
            sys.stderr.write("container %s not running\n" % (mycontainer_name))
            retval = False
        else:
            if role == 'instructor':
                if mycontainer_name == start_config.grade_container:
                    CopyChownGradesFile(mycwd, start_config, labtainer_config, mycontainer_name, mycontainer_image, container_user)
            else:
                GatherOtherArtifacts(labname, name, mycontainer_name, container_user)
                # Before stopping a container, run 'Student.py'
                # This will create zip file of the result
                baseZipFilename, currentContainerZipFilename = CreateCopyChownZip(mycwd, start_config, labtainer_config, mycontainer_name, mycontainer_image, container_user)
                ZipFileList.append(currentContainerZipFilename)
                print "baseZipFilename is (%s)" % baseZipFilename

            for mysubnet_name, mysubnet_ip in container.container_nets.items():
                disconnectNetworkResult = DisconnectNetworkFromContainer(mycontainer_name, mysubnet_name)

            # Stop the container
            StopMyContainer(mycwd, start_config, mycontainer_name)

    RemoveSubnets(start_config.subnets)

    if role == 'student':
        # Combine all the zip files
        #print "ZipFileList is "
        #print ZipFileList
        print "baseZipFilename is (%s)" % baseZipFilename
        xfer_dir = "/home/%s/%s" % (username, host_home_xfer)
        combinedZipFilename = "%s/%s.zip" % (xfer_dir, baseZipFilename)
        #print "The combined zip filename is %s" % combinedZipFilename
        zipoutput = zipfile.ZipFile(combinedZipFilename, "w")
        # Go to the xfer_dir
        os.chdir(xfer_dir)
        for fname in ZipFileList:
            basefname = os.path.basename(fname)
            zipoutput.write(basefname, compress_type=zipfile.ZIP_DEFLATED)
            # Remove after the file is zipped
            os.remove(basefname)
        zipoutput.close()

    return retval

def StopLab(labname, role):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
   
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, role)
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(LABTAINER_CONFIG, labname)
    host_home_xfer = labtainer_config.host_home_xfer

    # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
    host_xfer_dir = '%s/%s' % (myhomedir, host_home_xfer)
    CreateHostHomeXfer(host_xfer_dir)

    if DoStop(start_config, labtainer_config, mycwd, labname, role):
        # Inform user where results are stored
        print "Results stored in directory: %s" % host_xfer_dir
