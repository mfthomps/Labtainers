# first use dd if=/dev/zero of=wipefile bs=1024x1024; rm wipefile  on the VM
#vmware-vdiskmanager -k /home/mike/vmware/LabtainerVM-VMWare/LabtainerVM-VMWare-disk1.vmdk
/Applications/VMware\ Fusion.app/Contents/Library/vmware-vdiskmanager -k "$HOME/Virtual Machines.localized/Ubuntu 64-bit 24.04.vmwarevm/Virtual Disk.vmdk"

