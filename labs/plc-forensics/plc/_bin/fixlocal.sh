#!/bin/bash

cd $HOME
echo "Guest:guest" | sudo chpasswd
sudo systemctl enable httpserver.service
sudo systemctl start httpserver.service

