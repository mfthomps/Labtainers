from os import *
import os
import sys
import netifaces as ni
import time
from random import randint
import subprocess
import datetime
from datetime import timedelta

# IMPORT MODULES
import setup as s
import scans		# nmap scans and discovery
import mitm
import attacks		# catch-all file for short attacks.
import winxp		# contains ms08_067
from xss import xss
from sql import sql_injection
#from traffic import simulate_traffic


# ALIASING
printtime = s.printtime
printexpect = s.printexpect
getip = s.getip
log = s.log



# MAIN GLOBALS #
startip = 1

# Initialize the attacks
def initialize():

	global attack_no
	global attack_1
	global attack_2
	global attack_3
	global attack_4
	global attack_5
	global attack_6
	global attack_7
	global attack_8
	global attack_9
	global attack_10
	global attack_11
	
	attack_no = [1]
	attack_no[0] = 1 	# counter for attack numbers

	# This is where we define the attacks for the scenario 

	# Attack #1
	attack_1 = scans.nmap_os		# nmap OS discovery scans
	attack_1.time = 3			# length of attack in minutes
	attack_1.kali = s.kali1			# kali machine responsible for the attack
	attack_1.ip   = '192.168.1.43'		

	# Attack #2
	attack_2 = scans.nmap_stealth		# nmap stealth scans
	attack_2.time = 3
	attack_2.kali = s.kali1
        attack_2.ip   = '192.168.1.154'
	
	# Attack #3
	attack_3 = scans.nmap_proxychains	# nmap proxychains
	attack_3.time = 0
	attack_3.kali = s.kali1
        attack_3.ip   = '192.168.1.68'

	# Attack #4
	attack_4 = attacks.arp_poison		# MITM: arp poisoning
	attack_4.time = 5
	attack_4.kali = s.kali1
        attack_4.ip   = '192.168.1.72'

	# Attack #5
	attack_5 = attacks.ftp_https		# 16-21 ftp transfers behind proxies 
	attack_5.time = 0
	attack_5.kali = s.kali1
        attack_5.ip   = '192.168.1.81'

	# Attack #6
	attack_6 = attacks.ssh_brute		# 23-28 ssh distributed brute force
	attack_6.time = 0
	attack_6.kali = s.kali1
        attack_6.ip   = '192.168.1.99'

	# Attack #7
	attack_7 = attacks.ftp_brute		# 28-33 ftp brute force 
	attack_7.time = 5
	attack_7.kali = s.kali1
        attack_7.ip   = '192.168.1.127'

	# Attack #8
	attack_8 = attacks.ssh_login		# 33-38 SSH LOGIN
	attack_8.time = 0
	attack_8.kali = s.kali1
        attack_8.ip   = '192.168.1.163'

	# Attack #9
	attack_9 = winxp.ms08_067		# 40-45 MS08_067
	attack_9.time = 5
	attack_9.kali = s.kali1
        attack_9.ip   = '192.168.1.26'

	# Attack #10
	attack_10 = xss				# 45-53 xss
	attack_10.time = 8
	attack_10.kali = s.kali1
        attack_10.ip   = '192.168.1.187'
        
	# Attack #11
	attack_11 = sql_injection		# 53-61 sql injection
	attack_11.time = 8
	attack_11.kali = s.kali1
        attack_11.ip   = '192.168.1.141'

	

# CALL AN ATTACK
def attack(func):
	attacktime=func.time*s.counter
	if (s.kali_id == func.kali):
		system('echo "" >> timer.txt') # new line 
		printtime("Attack #"+str(attack_no[0])+" ("+str(func.time)+" minutes): "+func.desc)
                ipset = 'sudo ifconfig eth0 '+func.ip
                os.system(ipset)
                printtime("--Changed IP to "+func.ip)
	        func(attacktime)	# attack time
                attack_no[0] += 1

	else:
		time_now = 0
		system('echo "" >> timer.txt') # new line
		printexpect(str(attack_no[0]), str(time_now+func.time),  attacktime)



# SETUP: NETWORK DISCOVERY, SELF ID, ETC.
def setup():

	initialize()
	s.kali_id = 1

	system('service ssh start')
	system('sshpass -ptoor ssh -NfD 9050 root@localhost')
	time.sleep(3)

	s.startmain=time.time() # Reset timer		

def end():
    ip_end_set = 'sudo ifconfig eth0 192.168.1.100'
    os.system(ip_end_set)

# KALI#1 TELLS SECURITY ONION TO START SA TIMER
def startsatimer():
        printtime(" Startsatimer started here")
	if (s.kali_id == s.kali1):
                printtime("This is the correct Kali")
		try:	
			system('nc -v 192.168.1.13 8081')		# Signal Security Onion
			printtime("Told Security Onion to start the SA timer. (nc successful)")
		except:
			printtime("Failed to send nccommand to Security Onion")
	else:
		printtime("I am Kali #"+str(s.kali_id)+". Kali #1 is telling Security Onion to start the SA timer.")



##### MAIN #####
def main():

	# Start traffic generation
        subprocess.Popen(["python", "/root/Desktop/attacks/traffic.py"]) 


	# BUFFER
	system('echo "" >> timer.txt') # new line 
        printtime("Providing 7 minute buffer during scenario/SO setup")
        time.sleep(s.counter*7) 

	system('echo "" >> timer.txt') # new line 
	printtime("Expecting 3 minutes generic SA questions")
        time.sleep(s.counter*3) 

	system('echo "" >> timer.txt') # new line 
	printtime("Expecting 1 minute TLX1() after buffer on security onion")
	time.sleep(s.counter*1)	

	# NMAP SCANS
	attack(attack_1) # nmap_scans for 3 minutes

	attack(attack_2) # nmap_stealth for 3 minutes
	
	system('echo "" >> timer.txt') # new line 
	printtime("Expecting 3 minutes SA questions first()")
	time.sleep(s.counter*3)
       
	# ARP POISONING
	attack(attack_4) # arp_poisoning for 5 minutes

	system('echo "" >> timer.txt') # new line 
	printtime("Expecting 5 minutes SA questions second()")
	time.sleep(s.counter*5)
       
	system('echo "" >> timer.txt') # new line 
        printtime("Providing 2 minute buffer")
        time.sleep(s.counter*2) 

	# FTP BRUTE (EASY)
	attack(attack_7)  # ftp_brute for 5 minutes

	system('echo "" >> timer.txt') # new line 
	printtime("Expecting 3.5 minutes SA questions third()")
	time.sleep(s.counter*3.5)

	system('echo "" >> timer.txt') # new line 
	printtime("Expecting 1 minutes TLX2() after easy attack")
	time.sleep(s.counter*1)	

	system('echo "" >> timer.txt') # new line 
        printtime("Providing 2 minute buffer")
        time.sleep(s.counter*2) 

	# MSO8_067 (HARD)
	attack(attack_9) # ms08_067 for 5 minutes

	system('echo "" >> timer.txt') # new line 
	printtime("Expecting 5 minutes SA questions fourth()")
	time.sleep(s.counter*5)

	system('echo "" >> timer.txt') # new line 
	printtime("Expecting 1 minutes TLX3() after hard attack")
	time.sleep(s.counter*1)	

	system('echo "" >> timer.txt') # new line 
        printtime("Providing 2 minute buffer")
        time.sleep(s.counter*2) 

	# XSS
	attack(attack_10) # xss for 8 minutes

	system('echo "" >> timer.txt') # new line 
	printtime("Expecting 4.5 minutes SA questions fifth()")
	time.sleep(s.counter*4.5)

	system('echo "" >> timer.txt') # new line 
        printtime("Providing 2 minute buffer")
        time.sleep(s.counter*2) 

	# SQL
	attack(attack_11) # sql for 8 minutes

	system('echo "" >> timer.txt') # new line 
	printtime("Expecting 5 minutes SA questions sixth()")
	time.sleep(s.counter*5)

	system('echo "" >> timer.txt') # new line 
	printtime("All attacks and SA questions concluded")
        printtime("Changed IP to 192.168.1.100")
	
	log("\n #### SCENARIO COMPLETE ####")
        end()



########## Start Program ########## 
s.printbanner()

log("\n #### PRE-ATTACK SETUP ####")
setup()

log("\n #### ATTACK SETUP COMPLETE. TELL SECURITY ONION TO START SA TIMER ####")


log("\n #### START ATTACKS ####")
main()

# END OF FILE
