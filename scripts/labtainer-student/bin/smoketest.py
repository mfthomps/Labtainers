#!/usr/bin/env python
import subprocess
import os
import argparse
import shlex
import SimLab
import logging
import shutil
import filecmp
import ParseLabtainerConfig

class SmokeTest():
    def __init__(self):
        labtainer_config_path = os.path.abspath('../../config/labtainer.config')
        self.labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config_path, None)
        self.outfile = open('/tmp/smoke.out', 'w')
        logname = '/tmp/smoke.log'
        self.logger = logging.getLogger(logname)
        formatter = logging.Formatter('[%(asctime)s - %(levelname)s : %(message)s')
        file_handler = logging.FileHandler(logname)
        file_log_level = self.labtainer_config.file_log_level
        file_handler.setLevel(file_log_level)
        file_handler.setFormatter(formatter)

    def checkLab(self, lab):
        FAILURE=1
        retval = True
        xfer_dir = os.path.join(os.getenv('HOME'), self.labtainer_config.host_home_xfer, lab)
        print('xfer is %s' % xfer_dir)
        shutil.rmtree(xfer_dir, ignore_errors=True)
        os.mkdir(xfer_dir)
        cmd = 'start.py -q %s' % lab
        result = subprocess.call(cmd, shell=True, stderr=self.outfile, stdout=self.outfile)
        print 'result is %d' % result
        simlab = None
        if result == FAILURE:
            retval = False
        else:
            simlab = SimLab.SimLab(lab)
            if simlab is not None:
                simlab.simThis()
        cmd = 'stop.py %s' % lab
        ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1]) > 0:
            print('%s' % output[0])
            print('%s' % output[1])
            retval = False
        if retval and simlab is not None:
            here = os.getcwd() 
            os.chdir('../labtainer-instructor')
            cmd = 'start.py %s' % lab
            result = subprocess.call(cmd, shell=True, stderr=self.outfile, stdout=self.outfile)
            if result == FAILURE:
                retval = False
            print 'result is %d' % result
            cmd = 'stop.py %s' % lab
            result = subprocess.call(cmd, shell=True, stderr=self.outfile, stdout=self.outfile)
            if result == FAILURE:
                retval = False
            if retval:
                expected = simlab.getExpectedPath()
                if os.path.isdir(expected):
                    fname = '%s.grades.txt' % lab
                    new = os.path.join(xfer_dir, fname)
                    old = os.path.join(expected, fname)
                    if filecmp.cmp(new, old):
                        print('%s matches %s' % (new, old))        
                    else:
                        print('%s DOES NOT MATCH %s' % (new, old))        
                        retval = False
                    
       
        return retval
    
    def checkAll(self):
        
        skip_labs = os.path.abspath('../../../distrib/skip-labs')
        skip = []
        if os.path.isfile(skip_labs):
            with open(skip_labs) as fh:
                for line in fh:
                    f = os.path.basename(line).strip()
                    print('adding [%s]' % f)
                    skip.append(f)

        
        lab_parent = os.path.abspath('../../labs')
        lab_list = os.listdir(lab_parent)
        for lab in sorted(lab_list):
            if lab in skip:
                continue
            print('Start lab: %s' % lab)
            self.checkLab(lab)
            if not result:
                exit(1)
            print('Finished lab: %s' % lab)

def __main__():
    parser = argparse.ArgumentParser(description='Smoke test all labs')
    parser.add_argument('-l', '--lab', action='store', help='Test just this lab.')
    args = parser.parse_args()
    smoketest = SmokeTest()
    if args.lab is not None:
        smoketest.checkLab(args.lab)
    else:
        smoketest.checkAll()

if __name__=='__main__':
    __main__()
