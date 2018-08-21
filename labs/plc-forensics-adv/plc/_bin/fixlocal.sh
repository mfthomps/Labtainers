#!/bin/bash

cd $HOME
echo "Guest:guest" | sudo chpasswd
sudo systemctl enable httpserver.service
sudo systemctl start httpserver.service
echo "ftpd_banner=VxWorks FTP server (VxWorks VxWorks5.5) ready." | sudo tee -a /etc/vsftpd.conf
sudo systemctl restart vsftpd.service
