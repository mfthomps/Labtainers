#!/usr/bin/env python
import sys
done = False
running = False
while not done:
   cmd = raw_input("cadmin> ")
   if cmd == 'h' or cmd == 'help':
       print('start : enable the power distribution unit')
       print('stop  : disable the power distribution unit')
       print('status : show status of the power distirbution unit')
       print('exit : exit administrator tool')
   elif cmd == 'status':
       if running:
           print('Power distribution unit powered on')
       else:
           print('Power distribution unit powered off')
   elif cmd == 'start':
       print('Starting power distribution unit')
       running = True
   elif cmd == 'stop':
       print('Stopping power distribution unit')
       running = False
   elif cmd == 'exit':
       print('bye')
       exit(0)
   else:
       print('eh?')
