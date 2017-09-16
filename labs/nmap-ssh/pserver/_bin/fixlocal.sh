#!/usr/bin/env bash

sudo /etc/init.d/xinetd restart

echo 'ubuntu:NEWPWD' | sudo chpasswd
