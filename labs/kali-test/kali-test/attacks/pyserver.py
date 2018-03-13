# server.py 
import socket                                         
import time
from os import *


def callmain():
	system('echo "pyserver.py: calling main.py" >> timer.txt')
	system('python /root/Desktop/attacks/main.py')

system('sudo ifconfig eth0 192.168.1.1') # For testing only
system('echo "pyserver.py: started" > timer.txt')

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
#host = socket.gethostname()                           

port = 8080                                           

# bind to the port
serversocket.bind(('', port))                                  

# queue up to 5 requests
serversocket.listen(5)                                           

while True:
    	# establish a connection
    	clientsocket,addr = serversocket.accept()      
    	#print("Got a connection from %s" % str(addr))
	message = "Got a connection from %s" % str(addr)
	system('echo "pyserver.py: '+message+' - ok to start attacks" >> timer.txt')

	callmain()
    	currentTime = time.ctime(time.time()) + "\r\n"
    	clientsocket.send(currentTime.encode('ascii'))
    	clientsocket.close()


