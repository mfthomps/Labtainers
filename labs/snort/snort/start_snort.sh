#!/bin/bash
sudo snort -A console -q -c /etc/snort/snort.conf -i eth0 -k none
