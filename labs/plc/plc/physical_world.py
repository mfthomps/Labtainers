#!/usr/bin/env python
import ctypes
import mmap
import os
import struct
import time
import curses

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
def doMap(): 
    # Create new empty file to back memory map on disk
    # and return the buf associated with it
    print('try open %s' % filename)
    fd = os.open(filename, os.O_CREAT | os.O_TRUNC | os.O_RDWR)

    # Zero out the file to insure it's the right size
    assert os.write(fd, '\x00' * mmap.PAGESIZE) == mmap.PAGESIZE

    # Create the mmap instace with the following params:
    # fd: File descriptor which backs the mapping or -1 for anonymous mapping
    # length: Must in multiples of PAGESIZE (usually 4 KB)
    # flags: MAP_SHARED means other processes can share this mmap
    # prot: PROT_WRITE means this process can write to this mmap
    buf = mmap.mmap(fd, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE)
    return buf

def main(screen):
    flood = "The pond breached its banks and flooded the farmer's field"
    dry = "The low water level led to catfish mutations.  They walked into the farmer's fields and ate all the crops."
    clear = ' ' * 200
    buf = doMap()
    # Now create an int in the memory mapping
    water_level = ctypes.c_int.from_buffer(buf)
    pump_running = ctypes.c_int.from_buffer(buf, 4)
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
    screen.addstr(2,1, "Status of Farmer Jone's catfish pond water level")
    while True:
         if paused:
             screen.addstr(4,1, "Simulation paused, press space key to run     ")
             screen.refresh()
             c = screen.getch()
             if c == 32:
                 paused = not paused
             else:
                 time.sleep(1) 
             continue
         else:
             screen.addstr(4,1, "Simulation running, press space key to pause")
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
    
