from os import *
import sys
import time
import datetime
from datetime import timedelta

# IMPORT & ALIAS
import setup as s
printtime = s.printtime
funcprinttime = s.funcprinttime


counter=60	# 60 = 1 minute



#### NMAP OS DISCOVERY
def nmap_os(n):
	starttime=time.time()
	endtime = time.time()+n
	funcprinttime("  Start", starttime)

	command = "nmap -O -A -sV -sT 192.168.1.1-12"	#OS Detection, version detection
	while endtime>time.time():			

		# execute command		
		endtimer = str(endtime-time.time())
		system('timeout --kill-after='+endtimer+'s '+endtimer+'s '+command);
		funcprinttime("  - scan complete", starttime)

		# time remainder of attack
		timeleft = endtime-time.time()
		if timeleft>10:
			time.sleep(10)
	funcprinttime("  End",starttime)

nmap_os.desc = "nmap OS discovery scans"


#### NMAP STEALTH
def nmap_stealth(n):
	starttime=time.time()
	endtime = time.time()+n
	funcprinttime("  Start", starttime)

	command = "nmap -sS -p 21-23,25,139,3306,5432 192.168.1.2"
	while endtime>time.time():
	
		endtimer = str(endtime-time.time())
		system('timeout --kill-after='+endtimer+'s '+endtimer+'s '+command);
		funcprinttime("  - scan complete", starttime)

		timeleft = endtime-time.time()
		if timeleft>10:
			time.sleep(10)

	funcprinttime("  End", starttime)

nmap_stealth.desc = "nmap stealth scans"


#### NMAP PROXYCHAINS
def nmap_proxychains(n):
	starttime=time.time()
	endtime = time.time()+n
	funcprinttime("  Start", starttime)

	command = "proxychains nmap -p 21,22 -sV --version-light 192.168.1.2"
	while endtime>time.time():
		
		endtimer = str(endtime-time.time())
		system('timeout --kill-after='+endtimer+'s '+endtimer+'s '+command);
		funcprinttime("  - scan complete", starttime)
		
		timeleft=endtime-time.time()
		if timeleft>10:
			time.sleep(10)

	funcprinttime("  End", starttime)

nmap_proxychains.desc = "nmap proxychains"

# END OF FILE
