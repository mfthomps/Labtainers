#!/bin/bash
cd $HOME
gcc -m32 -fno-stack-protector -g -o vul_prog vul_prog.c
