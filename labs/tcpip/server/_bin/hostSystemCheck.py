#!/usr/bin/env python

import lsb_release
import subprocess
import sys

required_ubuntu_version = "16.04.2"

def isSortVsupported():
    command = 'echo -e "1.1.1\n1.1.2" | sort -V'
    ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1]) > 0:
        return 0 
    else:
        return 1 

def sortVstrings(string1, string2):
    command = 'echo "%s\\n%s" | sort -V | head -n 1' % (string1, string2)
    #print "command is (%s)" % command
    ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ps.communicate()
    answer = output[0].split()
    return answer

def version_lessthanequal(string1, string2):
    sorted_string = sortVstrings(string1, string2)
    #print "string1 is (%s) sorted_string is (%s)" % (string1, sorted_string[0])
    if (string1 == sorted_string[0]):
        return True
    else:
        return False

def version_lessthan(string1, string2):
    if (string1 == string2):
        return True
    else:
        return version_lessthanequal(string1, string2)

def CheckUbuntuVersion():
    #print "1.1.1 less than 1.1.1 is %s" % version_lessthan("1.1.1", "1.1.1")
    #print "1.1.2 less than 1.1.1 is %s" % version_lessthan("1.1.2", "1.1.1")
    #print "1.1.1 less than 1.1.2 is %s" % version_lessthan("1.1.1", "1.1.2")
    #print "1.2.1 less than 1.1.2 is %s" % version_lessthan("1.2.1", "1.1.2")

    lsb_info = lsb_release.get_lsb_information()
    lsb_info_id = lsb_info['ID']
    if (lsb_info_id == "Ubuntu"):
        no_sort = False
        if not isSortVsupported():
            no_sort = True

        ubuntu_description = lsb_info['DESCRIPTION']
        ubuntu_desc = ubuntu_description.split()
        ubuntu_version = ubuntu_desc[1]

        if no_sort or (ubuntu_version != required_ubuntu_version and version_lessthan(ubuntu_version, required_ubuntu_version)):
            print('Your Ubuntu version (%s) is older than %s, which is required in order to experiment with the\n')
            print('"sysctl" setting for syn_cookies".  This will not interfere with your ability to complete the lab.')
            return 1
    return 0

def main():
    check_ubuntu_version = CheckUbuntuVersion()
    return check_ubuntu_version

if __name__ == '__main__':
    sys.exit(main())

