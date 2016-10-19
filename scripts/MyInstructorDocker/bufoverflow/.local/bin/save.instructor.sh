#!/bin/bash

timestamp=$(date +"%Y%m%d%H%M%S")
tar -zcvf xfer.instructor.$timestamp.tar.gz `ls -d * .local | egrep -v tar.gz`
