#!/usr/bin/env python
#/****************************************************************************
#   Program:     $Id: tutorial1.py 2013-10-01 10:59:06Z rbeverly $
#   Description: CS4558 python dpkt tutorial2
#                Unfortunately, dpkt does not expose the pcap_version
#                and pcap_dlt_type functions in their API.  Here, we
#                dig into the bowels to get that capability.
#****************************************************************************/
import dpkt

f = open('bob.pcap')
b = f.read(dpkt.pcap.FileHdr.__hdr_len__)
fh = dpkt.pcap.LEFileHdr(b)
print "Snaplen:", fh.snaplen
print "Major version:", fh.v_major
print "Minor version:", fh.v_minor
print "DLT:", fh.linktype
