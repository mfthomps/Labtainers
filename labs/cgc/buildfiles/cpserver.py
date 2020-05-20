#!/usr/bin/env python
import os
import shutil
import glob
import stat
def writeService(service, path):
    sfile = os.path.join(path, service.lower())
    with open(sfile, 'w') as fh:
        fh.write('service %s\n' % service.lower())
        fh.write('{\n')
        fh.write('    flags = REUSE\n')
        fh.write('    socket_type = stream\n')
        fh.write('    wait = no\n')
        fh.write('    user = root\n')
        fh.write('    server = /usr/sbin/%s\n' % service)
        fh.write('    log_on_failure += USERID\n')
        fh.write('    log_on_success += USERID\n')
        fh.write('    disable = no\n')
        fh.write('}')

def copySource(source, source_dest, challenge):
    src = os.path.join(source, challenge,'src') 
    lib = os.path.join(source, challenge,'lib') 
    readme = os.path.join(source, challenge,'README.md') 
    readme_dst = os.path.join(source_dest, challenge,'README.md') 
    src_dst = os.path.join(source_dest, challenge,'src')
    shutil.copytree(src, src_dst)
    lib_dst = os.path.join(source_dest, challenge,'lib')
    if os.path.isdir(lib):
        shutil.copytree(lib, lib_dst)
    shutil.copyfile(readme, readme_dst)
    
    pov_list = glob.glob(os.path.join(source, challenge,'pov_*'))
    for pov in pov_list:
        cdir = os.path.join(source_dest, challenge, os.path.basename(pov))
        shutil.copytree(pov, cdir)
        print('copied %s' % pov)

def copyPolls(polls, client, challenge):
    dst = os.path.join(client, challenge, 'polls') 
    src = os.path.join(polls,challenge, 'poller', 'for-release')
    try:
        os.makedirs(dst)
    except:
        pass
    plist = glob.glob(src+'/*.xml')
    if len(plist) == 0:
        src = os.path.join(polls,challenge, 'poller', 'for-testing')
        plist = glob.glob(src+'/*.xml')
        
    for poll in plist:
        dst_poll = os.path.join(dst, os.path.basename(poll))
        shutil.copyfile(poll, dst_poll)

def copyPovs(build, client, challenge):
    src = os.path.join(build, challenge)
    plist = glob.glob(src+'/*.pov')
    print('client is %s' % client)
    dest_dir = os.path.join(client, challenge, 'povs')
    try:
        os.makedirs(dest_dir)
    except:
        pass
    for pov in plist:
        pdst = os.path.join(dest_dir, os.path.basename(pov))
        shutil.copyfile(pov, pdst)
        os.chmod(pdst, 0o755)

multios = '/home/mike/cb-mutios/cb-multios'
build = os.path.join(multios, 'build', 'challenges')
source = os.path.join(multios, 'challenges')
clist = os.listdir(source)
xinet_path = '../server/_system/etc/xinetd.d'
sbin_path = '../server/sys_tar/usr/sbin'
service_path = '../server/_system/etc/services'
shutil.copyfile(service_path+'.orig', service_path)
source_dest = '../server/home_tar/challenges'
try:
    shutil.rmtree(source_dest)
except:
    pass

client_challenges = '../client/home_tar/challenges'
service_map = '../client/service.map'
try:
    shutil.rmtree(client_challenges)
except:
    pass

polls = os.path.join(multios, 'polls')

serve_fh = open(service_path, 'a')
service_fh = open(service_map, 'w') 
port = 0xbaba

skip_fh = open('skiplist.txt') 
skip_list = []
for line in skip_fh:
    skip_list.append(line.strip()) 
    print('add <%s> to skiplist' % line.strip())
for challenge in sorted(clist):
    print('<%s>' % challenge)
    if challenge in skip_list:
        continue
    if not os.path.isdir(os.path.join(source, challenge)):
        continue
    ''' Create the service definition file '''
    writeService(challenge, xinet_path)
    ''' copy the executables '''
    sbin = os.path.join(sbin_path, challenge) 
    c_bin = os.path.join(build, challenge, challenge)
    shutil.copyfile(c_bin, sbin)
    os.chmod(sbin, 0o755)

    ''' add entry to the services file '''
    serve_fh.write('%s\t%d/tcp\n' % (challenge.lower(), port))
    ''' copy patched version '''
    sbin = os.path.join(sbin_path, challenge+'_patched') 
    c_bin = os.path.join(build, challenge, challenge+'_patched')
    shutil.copyfile(c_bin, sbin)
    os.chmod(sbin, 0o755)

    copySource(source, source_dest, challenge)
    copyPolls(polls, client_challenges, challenge)
    copyPovs(build, client_challenges, challenge)
    service_fh.write('%s\t\t%d\n' % (challenge, port))
    port += 1
    
service_fh.close()
serve_fh.close() 
