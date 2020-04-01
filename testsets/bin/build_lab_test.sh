#!/bin/bash

#Set email to frank@beans.com for SimLab.py
sed -i '1d' ~/.local/share/labtainers/email.txt
echo "frank@beans.com" >> ~/.local/share/labtainers/email.txt

#Reset the lab files
rm -rf ~/labtainer_xfer/wiggysinglebase


cd ../../labs
rm -fr wiggysinglebase
mkdir wiggysinglebase 
cd wiggysinglebase
new_lab_setup.py || exit 1
new_lab_setup.py -a firefox -b firefox || exit 1

cd wiggysinglebase
touch hello.py
echo "#!/usr/bin/env python" >> hello.py
printf "print('Hello World.')" >> hello.py
chmod +x hello.py

cd ../instr_config
echo "hello = wiggysinglebase:hello.py.stdout : CONTAINS : Hello World." >> results.config

cd ..

#Rebuild labs
cd ../../scripts/labtainer-student

echo "--Rebuild Single Base--"
rebuild wiggysinglebase || exit 1
stoplab
echo "--Smoketest Single Base--"
#SimLab.py wiggysinglebase
smoketest.py -l wiggysinglebase
