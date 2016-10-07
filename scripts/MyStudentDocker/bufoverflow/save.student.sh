#!/bin/bash

timestamp=$(date +"%Y%m%d%H%M%S")
tar -zcvf xfer.student.$timestamp.tar.gz `ls -d * .local | egrep -v tar.gz`
