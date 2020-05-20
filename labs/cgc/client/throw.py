#!/usr/bin/env python
import os
import multiprocessing as mp
import argparse
import sys
import socket
import struct
import random
import time

def _launch_pov_unix(pov, port, delay, pipe):
        # NOTE: This is running a forked process, free to clobber fds
        # This is mostly unchanged from the original source
        HOST = '172.25.0.3'  # The server's hostname or IP address

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.connect((HOST, port))
        time.sleep(delay)
        # Setup fds for communication
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(pipe.fileno(), 3)

        null = os.open('/dev/null', 0)
        os.dup2(null, 2)
        os.close(null)

        args = [pov]

        # Launch the POV
        os.execv(pov, args)
        exit(-1)

def read_all(fd, data_len):
        data = ''
        while len(data) < data_len:
            read = os.read(fd, data_len - len(data))
            assert len(read)
            data += read
        return data
def count_bits_set(value):
        count = 0
        while value:
            value &= value - 1
            count += 1
        return count


def launch_pov(pov, port, delay, pipe):
    pov_runner = mp.Process(target=_launch_pov_unix, args=(pov, port, delay, pipe))

    pov_runner.start()
    return pov_runner

def pov_negotiate(pipefd):
        MIN_BITS = 0


        data = read_all(pipefd, 4)
        pov_type = struct.unpack('<L', data)[0]
        assert pov_type in [1, 2], 'invalid pov type'


        if pov_type == 1:
            data = read_all(pipefd, 12)
            ipmask, regmask, regnum = struct.unpack('<LLL', data)
            accept = True

            if count_bits_set(ipmask) < MIN_BITS:
                print('not enough bits in IP mask')
                accept = False

            if count_bits_set(regmask) < MIN_BITS:
                print('not enough bits in REG mask')
                accept = False

            if regnum > 7:
                print('invalid GPR')
                accept = False

            if accept:
                ip = random.randint(0, 0xFFFFFFFF) & ipmask
                reg = random.randint(0, 0xFFFFFFFF) & regmask

                print('type 1 masks: %08x %08x' % (ipmask, regmask))
                print('type 1 pov: %08x %08x %d' % (ip, reg, regnum))

                pov_values = struct.pack('<LL', ip, reg)
                os.write(pipefd, pov_values)
        if pov_type == 2:
            PAGE_ADDR = 0x4347C000
            PAGE_LENGTH = 0x1000
            PAGE_BYTES = 4

            print("sending page location: %d, %d, %d" % (PAGE_ADDR, PAGE_LENGTH, PAGE_BYTES))
            pov_location = struct.pack('<LLL', PAGE_ADDR, PAGE_LENGTH, PAGE_BYTES)
            os.write(pipefd, pov_location)

            data = read_all(pipefd, 4)
            print("secret value: %s" % data.encode('hex'))




def doit(pov, port, delay):
        # Setup and run the POV
        pov_pipes = mp.Pipe(duplex=True)
        pov_runner = launch_pov(pov, port, delay, pov_pipes[1])

        pov_negotiate(pov_pipes[0].fileno())

        # Wait for the POV to finish and results to get logged
        pov_runner.join()

pov = sys.argv[1]
port = sys.argv[2]
delay = sys.argv[3]
print('throw %s port %s delay: %s' % (pov, port, delay))
doit(pov, int(port), int(delay))
