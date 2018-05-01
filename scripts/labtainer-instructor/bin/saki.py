#!/usr/bin/env python
import os
import sys
import zipfile
import shutil
instructor_cwd = os.getcwd()
student_cwd = instructor_cwd.replace('labtainer-instructor', 'labtainer-student')
# Append Student CWD to sys.path
sys.path.append(student_cwd+"/bin")
import ParseLabtainerConfig
import labutils
import LabtainerLogging


def extract(zip_fname, xfer, expect_lab):
    count = 0
    unexpected = 0
    with zipfile.ZipFile(zip_fname) as zip_file:
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            if filename.endswith('.zip'):
                parts = filename.split('.')
                lab = parts[-2]
                if lab == expect_lab:
                    count += 1
                else:
                    unexpected += 1
                lab_xfer = os.path.join(xfer, lab)
                # skip directories
                if not filename:
                    continue

                # copy file (taken from zipfile's extract)
                source = zip_file.open(member)
                target = file(os.path.join(lab_xfer, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
    if count > 0:
        print('Extracted %d student zip files' % count)
    if unexpected > 0:
        print('Extracted %d for other labs' % unexpected)
    
               

def checkBulkSaki(bulk_path = None, lab = None):
    labtainer_config_dir = '../../config/labtainer.config'
    labutils.logger = LabtainerLogging.LabtainerLogging("saki.log", 'none', labtainer_config_dir)
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config_dir, labutils.logger)
    home = os.getenv('HOME')
    xfer = os.path.join(home, labtainer_config.host_home_xfer)
    if bulk_path is None:
        bulk_path = os.path.join(xfer, 'bulk_download.zip') 
        if os.path.isfile(bulk_path):
            extract(bulk_path, xfer, lab)
        else:
            #print('no bulk file at %s' % bulk_path)
            pass
    else:
        if os.path.isfile(bulk_path):
            extract(bulk_path, xfer, lab)
        else:
            print('no file found at %s' % buld_path) 

if __name__ == '__main__':
    bulk = sys.argv[1]
    checkBulkSaki(bulk)
