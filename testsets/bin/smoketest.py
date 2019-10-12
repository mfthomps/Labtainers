#!/usr/bin/env python
import subprocess
import os
import sys
import argparse
import shlex
import SimLab
import logging
import shutil
import filecmp
sys.path.append('./bin')
import ParseLabtainerConfig
import labutils

class SmokeTest():
    def __init__(self, verbose_level):
        self.verbose_level = verbose_level
        labtainer_config_path = os.path.abspath('../../config/labtainer.config')
        self.labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config_path, None)
        self.simlab = None
        self.outfile = open('./smoke.out', 'w')
        logfilename = './smokex.log'
        logname = "smoketest"

        file_log_level = self.labtainer_config.file_log_level
        console_log_level = self.labtainer_config.console_log_level

        self.logger = logging.getLogger(logname)
        self.logger.setLevel(file_log_level)
        formatter = logging.Formatter('[%(asctime)s - %(levelname)s : %(message)s')

        file_handler = logging.FileHandler(logfilename)
        file_handler.setLevel(file_log_level)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_log_level)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        labutils.logger = self.logger
        self.logger.debug('Begin smoke test')

    def checkLab(self, lab, test_registry):
        FAILURE=1
        retval = True
        xfer_dir = os.path.join(os.getenv('HOME'), self.labtainer_config.host_home_xfer, lab)
        self.logger.debug('checkLab xfer is %s' % xfer_dir)
        shutil.rmtree(xfer_dir, ignore_errors=True)
        os.mkdir(xfer_dir)
        test_flag = ''
        if test_registry:
            test_flag = '-t'
        cmd = 'labtainer %s -q -r %s' % (lab, test_flag)
        result = subprocess.call(cmd, shell=True, stderr=self.outfile, stdout=self.outfile)
        self.logger.debug('result is %d' % result)
        self.simlab = None
        if result == FAILURE:
            retval = False
        else:
            self.simlab = SimLab.SimLab(lab, verbose_level=self.verbose_level, logger=self.logger)
            if self.simlab.hasSim():
                self.logger.debug('now call simLab')
                self.simlab.simThis()
        cmd = 'stoplab %s' % lab
        ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = ps.communicate()
        self.logger.debug('stoplab output %s' % output[0])
        email = labutils.getLastEmail()
        if email is not None:
            email = email.replace("@","_at_")
        if len(output[1]) > 0:
            print('%s' % output[0])
            print('%s' % output[1])
            retval = False
        if retval and self.simlab.hasSim():
            here = os.getcwd() 
            os.chdir('../labtainer-instructor')
            cmd = 'gradelab %s -r' % lab
            result = subprocess.call(cmd, shell=True, stderr=self.outfile, stdout=self.outfile)
            if result == FAILURE:
                retval = False
            self.logger.debug('instructor start result is %d' % result)
            '''
            self.simlab.searchWindows('GOAL_RESULTS')
            cmd = 'stop.py %s' % lab
            result = subprocess.call(cmd, shell=True, stderr=self.outfile, stdout=self.outfile)
            if result == FAILURE:
                retval = False
            self.logger.debug('instructor stop result is %d' % result)
            '''
            if retval:
                expected = self.simlab.getExpectedPath()
                if os.path.isdir(expected):
                    fname = '%s.grades.txt' % lab
                    new = os.path.join(xfer_dir, fname)
                    old = os.path.join(expected, fname)
                    if os.path.isfile(old):
                        if self.cmpStudent(new, old, email):
                            print('%s matches %s' % (new, old))        
                        else:
                            print('%s DOES NOT MATCH %s' % (new, old))        
                            retval = False
                    else:
                        print('no expected results for %s' % lab)
            os.chdir(here)
                    
       
        return retval

    def cmpStudent(self, new, old, email):
        new_line = None
        old_line = None
        with open(new) as new_fh:
            for line in new_fh:
                if line.strip().startswith(email):
                    new_line = line.strip().replace(" ", "")
                    break;
        with open(old) as old_fh:
            for line in old_fh:
                if line.strip().startswith(email):
                    old_line = line.strip().replace(" ", "")
                    break;
        if new_line != old_line:
            print('new: %s does not match\nold: %s' % (new_line, old_line))
            return False
        return True
    
    def checkAll(self, startwith, test_registry):
        
        skip_labs = os.path.abspath('../../distrib/skip-labs')
        skip = []
        if os.path.isfile(skip_labs):
            with open(skip_labs) as fh:
                for line in fh:
                    f = os.path.basename(line).strip()
                    print('adding [%s]' % f)
                    skip.append(f)
        skip.append('cyberciege')
        lab_parent = os.path.abspath('../../labs')
        lab_list = os.listdir(lab_parent)
        for lab in sorted(lab_list):
            if lab in skip:
                continue
            if startwith is not None and lab < startwith:
                continue
            print('Start lab: %s' % lab)
            sys.stdout.flush()
            result = self.checkLab(lab, test_registry)
            if not result:
                exit(1)
            print('Finished lab: %s' % lab)
            sys.stdout.flush()

def __main__():

    parser = argparse.ArgumentParser(description='Smoke test all labs')
    parser.add_argument('-l', '--lab', action='store', help='Test just this lab.')
    parser.add_argument('-s', '--start_with', action='store', help='Test all starting with .')
    parser.add_argument('-v', '--verbose', action='count', default=0, help="Use -v to see comments as they are encountered, -vv to see each line")
    parser.add_argument('-t', '--test_registry', action='store_true', default=False, help='Run with images from the test registry')

    args = parser.parse_args()
    smoketest = SmokeTest(args.verbose)
    if args.lab is not None:
        smoketest.checkLab(args.lab, args.test_registry)
    else:
        smoketest.checkAll(args.start_with, args.test_registry)

if __name__=='__main__':
    __main__()
