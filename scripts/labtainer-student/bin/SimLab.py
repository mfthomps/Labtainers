#!/usr/bin/env python
import os
import subprocess
import argparse
import time
global sim_path 
class SimLab():
    def __init__(self, lab):
        self.sim_path = os.path.abspath(os.path.join('../../../testsets/simlab', lab))
        if not os.path.isdir(self.sim_path):
            return None

    def getExpectedPath(self):
        return os.path.join(self.sim_path, 'expected')

    def dotool(self, cmd):
        cmd = 'xdotool %s' % cmd
        #print('dotool cmd: %s' % cmd)
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1]) > 0:
            print output[1]
        return output[0].strip()
    
    
    def searchWindows(self, name):
        wid = None
        while wid is None or len(wid) == 0:
            time.sleep(1)
            cmd = 'search %s' % name
            output=self.dotool(cmd)
            print('search out is %s' % output)
            wid = output.rsplit(' ',1)[0].strip()
            
        return wid
    
    def activate(self, wid):
        cmd = 'windowactivate --sync %s' % wid
        self.dotool(cmd)
    
    def typeLine(self, string):
        cmd = "type '%s'" % string
        self.dotool(cmd)
        #cmd = 'key Return'
        #self.dotool(cmd)
    
    def typeFile(self, fname):
        full = os.path.join(self.sim_path, fname)
        with open(full) as fh:
            for line in fh:
                if len(line.strip()) > 0:
                    self.typeLine(line)
                    time.sleep(0.5)

    def addFile(self, params, replace=False):
        from_file, to_file = params.split()
        from_file = os.path.join(self.sim_path, from_file) 
        cmd = 'vi %s' % to_file
        self.typeLine(cmd) 
        if replace:
            cmd = "type '9999dd'"
            self.dotool(cmd)
        self.dotool("type 'i'")
        with open(from_file) as fh:
            for line in fh:
                self.typeLine(line)
        self.dotool("key Escape")
        self.dotool("type 'ZZ'")
       
    
    def handleCmd(self, cmd, params):
        if cmd == 'window':
            wid = self.searchWindows(params)
            self.activate(wid)
        elif cmd == 'type_file':
            self.typeFile(params)
        elif cmd == 'add_file':
            self.addFile(params)
        elif cmd == 'replace_file':
            self.addFile(params, True)
    
    def simThis(self):
        exit(0)
        fname = os.path.join(self.sim_path, 'simthis.txt')
        print('smithThis for %s' % fname)
        with open(fname) as fh:
            for line in fh:
                if line.strip().startswith('#'):
                    continue
                #print line
                cmd, params = line.split(' ', 1)
                #print('cmd: %s params %s' % (cmd, params))
                self.handleCmd(cmd.strip(), params.strip())
                #print('back from handleCmd')


def __main__():
    parser = argparse.ArgumentParser(description='Simulate student performing lab')
    parser.add_argument('labname', help='The lab to simulate')
    args = parser.parse_args()
    lab = args.labname
    simlab = SimLab(lab)
    simlab.simThis() 

if __name__=="__main__":
    __main__()
