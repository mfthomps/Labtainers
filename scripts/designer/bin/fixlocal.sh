#!/bin/bash
cd $HOME
gcc -m32 -fno-stack-protector -o vul_prog vul_prog.c
