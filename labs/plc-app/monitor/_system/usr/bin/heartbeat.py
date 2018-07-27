#!/usr/bin/env python
import os
import time
cmd = 'manage_plc status'
while True:
    os.system(cmd)
    time.sleep(20)
    
