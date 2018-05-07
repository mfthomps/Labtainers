#!/usr/bin/env python
import os
import sys
import time
import zipfile
import shutil
from io import BytesIO
instructor_cwd = os.getcwd()
student_cwd = instructor_cwd.replace('labtainer-instructor', 'labtainer-student')
# Append Student CWD to sys.path
sys.path.append(student_cwd+"/bin")
import ParseLabtainerConfig
import labutils
import LabtainerLogging
'''
Extract individual zip files from a saki bulk download
'''

def extract(zip_fname, xfer, expect_lab):
    results_dir = os.path.join(xfer, expect_lab, 'reports')
    try:
        os.makedirs(results_dir)
    except OSError:
        pass
    count = 0
    unexpected = 0
    with zipfile.ZipFile(zip_fname) as zip_file:
        for member_info in zip_file.infolist():
            member = member_info.filename
            date_time = time.mktime(member_info.date_time + (0, 0, -1))
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

                # copy file (taken from zipfile's extract) into xfer for lab
                source = zip_file.open(member)
                target = file(os.path.join(lab_xfer, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)

                # copy reports
                parts = member.split('/')
                student = parts[1]
                target_dir = os.path.join(results_dir, student)
                zip_file_data = BytesIO(zip_file.read(member))
                with zipfile.ZipFile(zip_file_data) as zip_zips:
                   for zi in zip_zips.namelist():
                       if zi == 'docs.zip':
                           docs_zip_data = BytesIO(zip_zips.read(zi))
                           with zipfile.ZipFile(docs_zip_data) as zip_docs:
                               for zdoc_info in zip_docs.infolist():
                                   zdoc = zdoc_info.filename     
                                   doc_date_time = time.mktime(zdoc_info.date_time + (0, 0, -1))
                                   print('look for report in %s' % zdoc)
                                   fname, ext = os.path.splitext(zdoc)
                                   if (ext == '.docx' or ext == '.odg') and (fname+'.pdf' not in zip_docs.namelist()):
                                       if not os.path.isfile(os.path.join(target_dir, zdoc)):
                                           zip_docs.extract(zdoc, target_dir)
                                           print('extracted report %s to %s' % (zdoc, target_dir))
                                           os.utime(os.path.join(target_dir, zdoc), (doc_date_time, doc_date_time))
                                       else:
                                           print('found doc at %s, do not overwrite' % os.path.join(target_dir, zdoc))

            else:
                fname, ext = os.path.splitext(filename)
                if (ext == '.docx' or ext == '.odg'): 
                    source = zip_file.open(member)
                    parts = member.split('/')
                    student = parts[1]
                    target_dir = os.path.join(results_dir, student)
                    #print('target_dir is %s' % target_dir)
                    try:
                        os.makedirs(target_dir)
                    except OSError:
                        pass
                    #zip_file.extract(member, target_dir)
                    target = file(os.path.join(target_dir, filename), "wb")
      
                    #print('copied %s to %s' % (source, target))
                    shutil.copyfileobj(source, target)
                    os.utime(os.path.join(target_dir, filename), (date_time, date_time))
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
