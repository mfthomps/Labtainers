#!/bin/bash

gcc -m32 -o call_shellcode -fno-stack-protector -z execstack call_shellcode.c
gcc -m32 -o exploit -fno-stack-protector -z execstack exploit.c
#gcc -m32 -o stack -fno-stack-protector -z execstack stack.c
gcc -g -m32 -o stack -fno-stack-protector -z execstack stack.c
sudo chown root:root stack
sudo chmod 4755 stack
