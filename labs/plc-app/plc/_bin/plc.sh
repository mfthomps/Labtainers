#!/bin/bash
./plc_loader.py > loader.log 2>&1 & 
./physical_world.py
exit
