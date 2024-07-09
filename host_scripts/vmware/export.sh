#!/bin/bash
rm -f ./LabtainerVM-VMWare.ova
"/Applications/VMware Fusion.app/Contents/Library/VMware OVF Tool/ovftool" "$HOME/Virtual Machines.localized/Ubuntu 64-bit 24.04.vmwarevm/Ubuntu 64-bit 24.04.vmx" ./LabtainerVM-VMWare.ova
#rm -f /VMs/LabtainerVM-2-VMware/LabtainerVM-VMware-test*
#ovftool -o --lax -n=LabtainerVM-VMware-test LabtainerVM-VMWare.ova /VMs/LabtainerVM-2-VMware/LabtainerVM-2-VMware/LabtainerVM-VMware-test.vmx
#RESULT=$?
#if [ $RESULT -eq 0 ];then
#    vmrun start /VMs/LabtainerVM-2-VMware/LabtainerVM-2-VMware/LabtainerVM-VMware-test.vmx
#else
#    echo "Failed to build test VM"
#fi

