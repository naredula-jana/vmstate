#!/usr/bin/env python2
"""
/*
* This program is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 2 of the License, or
* (at your option) any later version.
*
*   main.py
*   Naredula Janardhana Reddy  (naredula.jana@gmail.com, naredula.jana@yahoo.com)
*
*/
"""
import vmstate,sys
import getopt
import subprocess
import sys
import argparse
import os
import tempfile
import errno

def main(options):
    global mem_file
    try:
        print options
        mem_file = open(options.file_phymemmap, 'wb') 
        snapshot_file = open(options.qemu_snapshot, 'rb')
        sys.stdout = open(options.file_devicestate, 'w')
        vmstate.read(snapshot_file,mem_file)
    except IOError:
        print "Error: can\'t find file to read data"
        return 1;


    mem_file.close()
    print "<args>"
    args = [
            "%s"%(options.file_phymemmap),""
            "%s"%(options.qemu_snapshot),""
            "%s"%(options.file_kernelcore),""
            ]
    print args
    print "</args>"
    subprocess.call(["./generate_elf"] + args  )
    print "<extra_output>"
    vmstate.read_phy_mem(0x102000)
    vmstate.read_phy_mem(0x101000)
    vmstate.read_phy_mem(0x101000)
    vmstate.read_phy_mem(0x103000)
    print "</extra_output>"

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(prog='main')
    parser.add_argument("-s", "--qemu_snapshot", action="store", default="../bin/jiny_snapshot",
                        help="qemu snapshot file ")
    parser.add_argument("-d", "--file_devicestate", action="store", default="file_devicestate.xml",
                        help="device state stored in this file")
    parser.add_argument("-m", "--file_phymemmap", action="store", default="file_memmap",
                        help="device state stored in this file")
    parser.add_argument("-k", "--file_kernelcore", action="store", default="file_kernel_core",
                        help="kernelcore")
    
    cmdargs = parser.parse_args()
    main(cmdargs)     