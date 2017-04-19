#!/bin/bash
#
# Compile programs associated with the SEED Buffer Overflow lab.
#
#
# Example program that transfers execution to its own stack
# to execute shell code.  Compile with option to permit execution
# from the stack.
#
gcc -m32 -o call_shellcode -z execstack call_shellcode.c
#
#  Program that writes the "bad file".
#  This is the program the student modifies to craft the
#  bad file to cause the buffer overflow.
#
gcc -m32 -o exploit exploit.c
#
# compile the vulnerable program with no stack protector
# and allow execution from the stack
#
gcc -g -m32 -o stack -fno-stack-protector -z execstack stack.c
sudo chown root:root stack
sudo chmod 4755 stack
