#!/bin/bash
cd $HOME
gcc -fno-stack-protector -g -o vul_prog vul_prog.c
