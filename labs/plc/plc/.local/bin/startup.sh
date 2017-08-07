#!/bin/bash
LOCKDIR=/tmp/.mylockdir
if mkdir "$LOCKDIR" >/dev/null 2>&1; then
    ./plc_loader.py > loader.log 2>&1 & 
    ./physical_world.py
fi
