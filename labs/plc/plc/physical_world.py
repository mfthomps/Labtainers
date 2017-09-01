#!/usr/bin/env python
import ctypes
import mmap
import os
import struct
import time
import curses
import logging
'''
This python script represents the physical system.  It interacts with
the PLC via shared memory.  The physical system has two active attributes.
The first is a source of water flowing into a resevoir at a rate that
varies over time.  The second is an outflow drain pump that is either on or off, 
controlled by the PLC. When open, the pump removes 2 vertical feet per day
from the resevior.  Everything
is measured in feet per day, and there is one day of simulated time per second
of real time.
 
Shared memory represents an I/O device connecting the simulated PLC to the physical
system. The first 32-bit int represents the current water level, and is written by a physical 
system monitor to shared memory.  The second 32-bit int 
is an input from the PLC, which is true if the pump is running, false if closed.
'''

filename='/tmp/iodevice'
log_30 = 0
log_20 = 0
count_resets = 0
LOGFILE = "./phys_world.log"
print("logging to %s" % LOGFILE)
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)
logging.debug("Starting physical_world")

def doMap(): 
    # Create new empty file to back memory map on disk
    # and return the buf associated with it
    print('try open %s' % filename)
    while not os.path.isfile(filename):
        time.sleep(1)
    fd = os.open(filename, os.O_RDWR)

    # Create the mmap instace with the following params:
    # fd: File descriptor which backs the mapping or -1 for anonymous mapping
    # length: Must in multiples of PAGESIZE (usually 4 KB)
    # flags: MAP_SHARED means other processes can share this mmap
    # prot: PROT_WRITE means this process can write to this mmap
    buf = None
    while buf is None:
        try:
            buf = mmap.mmap(fd, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE)
        except:
            time.sleep(1)
    logging.debug("physical_world, file mapped")
    return buf

def logWaterLevel(water_level, reset_counter):
    retval = False
    global log_20
    global log_30
    global count_resets
    if count_resets != reset_counter:
        count_resets = reset_counter
        log_30 = 0
        log_20 = 0
   
    if water_level == 30:
        log_30 += 1
    if water_level == 20:
        log_20 += 1
    if log_30 == 4 and log_20 == 4:
        with open('water_level.log', 'w') as fh:
            fh.write('PLC Secured\n')
        retval = True
    return retval

def main(screen):
    log_close = False
    flood = "The pond breached its banks and flooded the farmer's field"
    dry = "The low water level led to catfish mutations.  They walked \ninto the farmer's fields and ate all the crops."
    success = "Well done! You have protected the farm's infrastructure.  \nThe lab is completed."
    clear = ' ' * 200
    buf = doMap()
    # Now create an int in the memory mapping
    water_level = ctypes.c_int.from_buffer(buf)
    pump_running = ctypes.c_int.from_buffer(buf, 4)
    loader_ready = ctypes.c_int.from_buffer(buf, 8)
    reset_counter = ctypes.c_int.from_buffer(buf, 12)
    while loader_ready.value == 0:
        time.sleep(1)
    logging.debug("physical_world,  loader must be ready")
    water_level.value = 20
    ''' rate of water leaving via drain (when open)'''
    out_flow_rate = 2
    ''' rate of water coming in '''
    in_flow_rate = 1
    curses.noecho()
    curses.cbreak()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    screen.bkgd(curses.color_pair(2))
    #screen.keypad(1)
    screen.nodelay(1)
    screen.refresh()
    #win = curses.newwin(5,20,5,5)
    #win.bkgd(curses.color_pair(2)) 
    #win.box()
   
    paused = False 
    screen.addstr(2,1, "Status of Farmer Jones' catfish pond water level")
    lab_success = False
    while True:
         if not lab_success:
             lab_success = logWaterLevel(water_level.value, reset_counter.value)
         if pump_running.value == 1 and water_level.value > 0:
             water_level.value -= out_flow_rate 
             #print('pump running')
             screen.addstr(8,1, "Pump: running")
         else:
             screen.addstr(8,1, "Pump: stopped")
         if water_level.value < 42:
             water_level.value += in_flow_rate
         screen.addstr(11,1, "Pond water level: %4d" % water_level.value)
         #print('current level is %s' % water_level.value)
         if water_level.value > 40:
             screen.addstr(15,1, flood) 
         elif water_level.value < 5:
             screen.addstr(15,1, dry) 
         elif lab_success:
             screen.addstr(15, 1, success)
         else:
             screen.addstr(15,1,clear)
         screen.refresh()
         c = screen.getch()
         if c == 32:
             paused = not paused
         time.sleep(1)
    raw_input("any key to end")

try:   
    curses.wrapper(main) 
except KeyboardInterrupt:
    print('keyboard exception, bye')
    exit()
    
