#!/bin/bash
#
# Compile programs associated with the buf64 lab
#
#
#  Program that writes the "bad file".
#  This is the program the student modifies to craft the
#  bad file to cause the buffer overflow.
#
gcc -o exploit exploit.c
#
# compile the vulnerable program with no stack protector
# and allow execution from the stack
#
gcc -g  -o stack -fno-stack-protector -z execstack stack.c
