#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
sudo sed -i s!/var/log/ulog/syslogemu.log!/var/log/iptables.log! /etc/ulogd.conf
sudo systemctl restart ulogd2
