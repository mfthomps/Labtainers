#!/bin/bash
labdir=`dirname "$0"`
BACK_STORE=$labdir/usb.img
echo "backstore is $BACK_STORE"
modprobe g_mass_storage file=$BACK_STORE idVendor=0x1d6b idProduct=0x0104 iManufacturer=Myself iProduct=VirtualBlockDevice iSerialNumber=123
