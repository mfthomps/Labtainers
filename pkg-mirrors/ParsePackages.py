#!/usr/bin/env python
'''
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
'''

import os
import sys
import re
import AddPkgLogging

''' logger is defined in whatever script that invokes this '''
global logger

class ParsePackages():
    def __init__(self, pkgname):
        self.pkginfo = {} # dictionary of package's info
        self.pkgname = pkgname

        if not os.path.exists(pkgname):
            logger.ERROR("Config file %s does not exists!" % pkgname)
            sys.exit(1)

        self.parsepkg(pkgname)

    class PackageInfo():
        def __init__(self, fname, deplist):
            self.fname = fname
            self.deplist = deplist

    def parsepkg(self, pkgname):
        keywords = {"package","filename","depends"}
        with open(pkgname, "r") as f:
            found_pkg = False
            previousline_end_with_comma = False
            for line in f:
                linestrip = line.strip()
                if not linestrip or linestrip.startswith("#"):
                    continue
                if not previousline_end_with_comma:
                    keyval = linestrip.split(':', 1)
                    key = keyval[0].lower()
                    if len(keyval) > 1:
                        val = keyval[1].lower().strip()
                else:
                    val = linestrip.strip()

                if not found_pkg:
                    # If haven't found the "Package: <pkgname>" skip until found
                    if key == "package":
                        found_pkg = True
                        pkgname = val
                        fname = ""
                        deplist = []
                    else:
                        continue
                else:
                    # If found the next "Package: <pkgname>", store the previous info
                    if key == "package":
                        self.pkginfo[pkgname] = self.PackageInfo(fname, deplist)
                        pkgname = val
                        fname = ""
                        deplist = []
                    elif key == "filename":
                        fname = val
                    elif key == "depends":
                        dependencies = val.split(',')
                        for dependency in dependencies:
                            deplist.append(dependency.strip())
                    else:
                        # Only interested in "package", "filename" and "depends"
                        continue
                        
                if val.endswith(','):
                    previousline_end_with_comma = True
                else:
                    previousline_end_with_comma = False

    def GetPackages(self):
        return self.pkginfo

    def show_current_settings(self):
        bar = "="*80
        print bar
        print("Package configuration settings:")
        print bar
        for name, package in self.pkginfo.items():
            print "package: " + name 
            for key, val in package.__dict__.items():
                if type(val) == type({}): val = len(val)
                print "\t" + str(key) + ": " + str(val)
            print ""
             
if __name__ == '__main__':
    start_config = ParsePackages(*sys.argv[1:])
    start_config.show_current_settings()
