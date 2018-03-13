#!/usr/bin/python
#
#This File simply calls tcpreplay for traffic replay, main releases the subprocess and ends when the scenario is over.

import sys
import netifaces as ni
import time
from random import randint
import subprocess
import datetime
from datetime import timedelta

from os import * 

# This function replays a pcap file	
def traffic_replay(pcap):
	print "Starting Traffic..."
        system('tcpreplay --pps=3 --loop=0 --intf1=eth0 /root/Desktop/attacks/pcap/traffic_scenario.pcapng& sleep '+str(90*60)+'; kill $!') 

# Method to thread pcap replays to simulate a flood of network traffic
def simulate_traffic():

	global path
	path = '/root/Desktop/attacks/'	
	try:
		
		# TRAFFIC 
                traffic_replay('traffic_scenario.pcapng')

	except:
		print "Error: could not start threads" 


simulate_traffic() 

# END OF FILE
