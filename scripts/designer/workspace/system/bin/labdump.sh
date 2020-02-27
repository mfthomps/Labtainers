#!/bin/bash

sudo /usr/bin/tcpdump -U -w - -i $1 | /bin/labdump_client.py $2 $3 $4
sleep infinity

