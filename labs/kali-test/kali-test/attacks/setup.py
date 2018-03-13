import os
import sys
import netifaces as ni
import time
from random import randint
import subprocess
import datetime
from datetime import timedelta

# SETUP GLOBALS
hosts = []
global startmain
startmain = time.time()
global counter
counter = 60	# 1=seconds, 60=1 minute

global kali_id
global kali1

kali_id = 0 # which attacking machine am i?
kali1 = 1



def printbanner():
	os.system("echo '\
-----------------------------------------\n\
| CHLICSA Cyber Defense Attack Scenario |\n\
-----------------------------------------\n' >> timer.txt")
	

# Print status and timestamp to log file
def printtime(desc): # print comment + timestamp
	#import main as m
	elapsed = str(timedelta(seconds=(time.time()-startmain))).split('.',2)[0]
	clocktime = str(time.strftime("%H:%M:%S"))
	os.system('echo "['+clocktime+'] ['+elapsed+'] '+desc+'" >> timer.txt')


# Print status from within function (omits clock time for cleaner log file)
def funcprinttime(desc, funcstarttime):
	elapsed = str(timedelta(seconds=(time.time()-funcstarttime))).split('.',2)[0]
	os.system('echo "              ['+elapsed+'] '+desc+'" >> timer.txt')


# Wait while attacks are being handled by other machines 
def printexpect(expect, timerange, zzz): 
	printtime("Expecting Attack #"+expect+" from "+timerange+" minutes.")
	#import main as m
	time.sleep(zzz*counter)


# Print unformatted text to log
def log(desc):
	os.system('echo "'+desc+'" >> timer.txt')


# Returns the current IP address **Still need
def getip():
        ni.ifaddresses('eth0')                          #interface is eth0
        myip= ni.ifaddresses('eth0')[2][0]['addr']      #get ip
        return myip

# END OF FILE
