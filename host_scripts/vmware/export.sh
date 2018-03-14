#!/bin/bash
rm -f ./LabtainerVM-VMWare.ova
ovftool /home/mike/vmware/LabtainerVM-VMWare/LabtainerVM-VMWare.vmx ./LabtainerVM-VMWare.ova
rm -f /home/mike/vmware/LabtainerVM-VMWare/LabtainerVM-VMWare-test*
ovftool -n=LabtainerVM-VMWare-test LabtainerVM-VMWare.ova /home/mike/vmware/LabtainerVM-VMWare/LabtainerVM-VMWare-test.vmx
vmrun start /home/mike/vmware/LabtainerVM-VMWare/LabtainerVM-VMWare-test.vmx

