#!/usr/bin/python
"""
/*
* This program is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 2 of the License, or
* (at your option) any later version.
*
*   read_vmstate.py
*   Naredula Janardhana Reddy  (naredula.jana@gmail.com, naredula.jana@yahoo.com)
*
*/
"""
import struct
import device_database
import sys, traceback, os

DEBUG = False
PAGE_MASK = 0xffffff00
MEMORY_UNCOMPRESSED = 0xfff # compressed byte take value from 0 to 0xff
def log(s):
    if DEBUG:
        print s

def qemu_get_ubyte():
    global f
    v = struct.unpack('>B', f.read(1))
    return (v[0])

def qemu_get_byte():
    global f
    try:
        v = struct.unpack('>b', f.read(1))
        return (v[0])
    except struct.error:
        raise
    

def qemu_get_be16():
    global f
    try:
        v = struct.unpack('>H', f.read(2))
    except struct.error:
        raise
    return v[0]

def qemu_get_be32():
    global f
    try:
        v = struct.unpack('>I', f.read(4))
    except struct.error:
        raise
    return v[0]

def qemu_get_be64():
    global f
    try:
        ui = struct.unpack('>Q', f.read(8))
    except struct.error:
        raise
    return ui[0];

def qemu_get_string(len):
    global f
    try:
        mstr = struct.unpack("<"+str(len)+"s", f.read(len))
    except struct.error:
        raise
    return mstr

def read_elements(name,element_list):
    print ' <subdevice><name>%s</name>'%(name)
    for element in element_list:
        if (element[1]==1):
            v=qemu_get_byte();
            print "    <element><name>%s</name><value>%x</value></element>"%(element[0],v)
        elif (element[1]==2):
            v=qemu_get_be16()
            print "    <element><name>%s</name><value>%x</value></element>"%(element[0],v)
        elif (element[1]==4):
            v=qemu_get_be32()
            print "    <element><name>%s</name><value>%x</value></element>"%(element[0],v) 
        elif (element[1]==8):
            v=qemu_get_be64()
            print "    <element><name>%s</name><value>%x</value></element>"%(element[0],v) 
    print " </subdevice>" 
    return v

virtio_dev = [['status',1],['isr',1],['queue_sel',2],['quest_features',4],['config_len',4]]
virtio_ring = [['vring_num',4],['pa',8],['last_avil_idx',2],['pci_vector',2]]
virtio_net1 = [['vqs_tx_waiting',4],['mergeable_rx_bufs',4],['status',2],['promisc',1],['allmulti',1],['mac_table_in_use',4]]
def read_virtio(max_to_read):
    global f
    """327 bytes pci load config , virtio_pci_load_config (d=0x555556f62920, f=0x5555570cd340)
     at hw/virtio/virtio-pci.c:144"""
    f.seek(device_database.VIRTIO_PCI_SIZE,1)
    print "<device>virtio</device>"
    len=read_elements("virtio_dev_",virtio_dev)
    config = qemu_get_string(len)
    max_queues = qemu_get_be32()
    print '   <element><name>max queues</name><value>%x</value></element>'%(max_queues)
    for x in xrange(1, max_queues+1): 
        len=read_elements("virtio_ring_",virtio_ring)
    mac0 = qemu_get_ubyte()
    mac1 = qemu_get_ubyte()
    mac2 = qemu_get_ubyte()
    mac3 = qemu_get_ubyte()
    mac4 = qemu_get_ubyte()
    mac5 = qemu_get_ubyte()
    print '    <element><name>mac</name><value>%x:%x:%x:%x:%x:%x</value></element>'%(mac0,mac1,mac2,mac3,mac4,mac5)
    len=read_elements("virtio_net_",virtio_net1)
    return  

def read_virtio_net(device):
    global f
    before_offset = f.tell()
    field=device[0]
    fname = field[0]
    fsize = field[1]
    fnum = field[2] 
    fversion = field[3] 
    hardcoded_size=fnum
    read_virtio(hardcoded_size)
    bytes_read = f.tell() - before_offset
    log('bytes read:%d hardcodesize:%d'%(bytes_read,hardcoded_size))
    if (bytes_read < hardcoded_size):
        f.seek(hardcoded_size-bytes_read,1)
    return

def read_subsection():
    global f
    #print " READING subsection for device ";
    type=qemu_get_byte();
    if (type != 0x05):
        f.seek(-1,1)
        return

    len = qemu_get_byte();
    estr = struct.unpack("<"+str(len)+"s", f.read(len))
    version_id = qemu_get_be32();
    log ('SUBSECTION device element :%s version:%d'%(estr,version_id))
    sys.exit(6)
    return;

def get_device(name):
    for row in device_database.device_list:
        if ((name.endswith(row[0][0]) and row[0][0][0]=='/') or (name == row[0][0])):
            return row
    return 0

def device_size(device):
    i=0;
    total_size=0
    for field in device:
        fname = field[0]
        fsize = field[1]
        fnum =  field[2] 
        if (fnum ==0):
            fnum=1
        i=i+1
        if (i == 1):
            continue
        total_size = total_size+fsize*fnum
    return total_size
  
def read_device(name,arg_version):
    global f
    global mem_file
    totalsize=0
    device=get_device(name);
    print "<device><inst_name>%s</inst_name><offset>%d</offset>"%(name,f.tell())
    if (device ==0):
        print "<error> device not found in the database :%s</error>"%(name)
        traceback.print_exc(file=sys.stdout)
#       sys.exit(5)
        return;
    i=0;
# TODO : check virtio not the exact name of device 
    if (name == '0000:00:03.0/virtio-net'):
        read_virtio_net(device)
        return;
    
    for field in device:
        fname = field[0]
        fsize = field[1]
        fnum =  field[2] 
        fversion = field[3] 
        foffset = field[4] 

        if (fnum == 0):
            fnum=1

        if (i==0): # first row is overloaded to store the device details
            hardcodedsize = fnum
            dsize = device_size(device)
            if (hardcodedsize != 1):
                dsize = hardcodedsize
            foffset_start = f.tell()
            print "  <name>%s</name><version>%d</version><in_vers>%d<in_version><size>%d(%d)</size>"%(fname,fversion,arg_version,hardcodedsize,dsize)
        else:
            tsize = (fsize*fnum);
            val = 0x0
            if ((fsize+foffset) > (dsize)):
                print "  <element><name>%s</name><off>%d</off><size>%d*%d</size><version>%d</version><status>SKIPING</status></element>"%(fname,foffset,fsize,fnum,fversion)
            else:
                f.seek(foffset_start+foffset)
                if (fsize == 8):
                    val = qemu_get_be64()
                elif (fsize == 4):
                    val = qemu_get_be32()
                elif (fsize == 2):
                    val = qemu_get_be16()
                elif (fsize > 8):
                    val = qemu_get_be64()
                print "  <element><name>%s</name><off>%d</off><foff>%x</foff><size>%d*%d</size><version>%d</version><value>%x</value></element>"%(fname,foffset,f.tell(),fsize,fnum,fversion,val)
                f.seek(foffset_start+foffset)
                if(fname == "env.regs" or fname == "env.cr[3]"):
                    values =1;
                    if (fname == "env.regs"):
                        values = 16
                    elif (fname == "env.regs"):
                        values = 1
                        
                    print_field = 1
                    mem_file.write(" %s "%(fname))
                    for x in xrange(1, values+1):
                        val = qemu_get_be64();
                        mem_file.write("%x "%(val))
                        print "     %x"%(val)
                    mem_file.write("\n");
        i=i+1
    if (i>=0):
        f.seek(foffset_start+dsize)
    #print "   total size : %d  filepos:%d"%(dsize,f.tell())
    read_subsection()
    print "</device>\n"
    return

phy_mem = []
phy_index=0
def read_phy_mem(target_addr):
    global f
    for p in xrange(1, phy_index):
        (phy_addr,offset,compressed)= phy_mem[p]
        if (phy_addr == (target_addr&PAGE_MASK)):
            if (compressed != MEMORY_UNCOMPRESSED):
                value = compressed
                print "compressed memory found :",value
                return value
            f.seek(offset)
            value = qemu_get_be64()
            print " offset : %x value  %x->%x:%x:%x  offset:%x"%(f.tell()-8,target_addr,value,qemu_get_be64(),qemu_get_be64(),f.tell())
            return value
    print "ERROR Unable to find .."
    return 0

lowest_addr=0
highest_addr=0
def read_mem():
    global f,phy_mem,phy_index
    global lowest_addr
    global highest_addr
    global mem_file
    
    flags = 0x1
    while(flags != 0x10):
        addr = qemu_get_be64()
        flags = addr & 0xff
        if (flags & 0x4): # ram sizes  RAM_SAVE_FLAG_MEM_SIZE
            i=0
            total_mem = 0xff
            while (total_mem < addr):
                len = qemu_get_byte()
                idstr, length = struct.unpack(">" + str(len) + "sQ", f.read(len + 8))
                i = i + 1
                total_mem = total_mem + length
                print '%3d:  %35s: length:%9x(%9dM) flags:%x '%(i, idstr, length,length/(1024*1024),flags)
            print 'Ram Sizes Total mem :%10x  flags:%x' %(total_mem,flags)
        elif ((flags & 0x8) or (flags & 0x02)): # ram page RAM_SAVE_FLAG_PAGE or RAM_SAVE_FLAG_COMPRESS
            compress_byte=MEMORY_UNCOMPRESSED
            if (flags & 0x20): # ram flag continue
                len=0 
                file_offset = f.tell()
                if (addr > highest_addr):
                    highest_addr = addr
                if (flags & 0x02): #RAM_SAVE_FLAG_COMPRESSmem_file
                    compress_byte = qemu_get_byte()
                    log("mem page addr :%x  offset:%x :%d  flags:%x compressByte: %x"%(addr,f.tell(),f.tell(),flags,compress_byte));
                else:
                    f.seek(4096,1)
                    log("mem page addr :%x  offset:%x :%d  flags:%x"%(addr,f.tell(),f.tell(),flags));
                mem_file.write(" %x %x %x \n"%(addr,file_offset,compress_byte))
            else:
                len = qemu_get_byte();
                mstr = struct.unpack("<"+str(len)+"s", f.read(len))
                print "%40s highest addr :%x"%("",highest_addr)
                print "%35s file offset: %8x :%8dM address:%9x"%(mstr,f.tell(),f.tell()/(1024*1024),addr)
                log("mem page addr :%x "%(addr));
                highest_addr = 0x0
                file_offset = f.tell()
                if (flags & 0x02): #RAM_SAVE_FLAG_COMPRESS
                    compress_byte = qemu_get_byte()
                else:
                    f.seek(4096,1)
            # store the page details in the list for further access
            phy_mem.append([])
            phy_mem[phy_index] = [addr&PAGE_MASK,file_offset,compress_byte];
            #print " phy_index:%x addr:%x compressed:%x"%(phy_index,addr&PAGE_MASK,compress_byte)
            phy_index = phy_index+1

        elif (flags & 0x80): # ram end RAM_SAVE_FLAG_EOS
            printf(" ERROR: RAM FLAG SAVE HOOK")
            return
        elif (flags & 0x10): # ram end RAM_SAVE_FLAG_EOS
            log ("End of Memory :%x"%(addr))
            return
        else:
            print "ERROR: ram unrecognised flags: %x"%(flags) 
            sys.exit(4)
            return;
    
    return;

def read(in_file, m_file):
    global f
    global mem_file
    f = in_file;
    mem_file = m_file
    first_device=1
    x,version = struct.unpack('>4si', f.read(8))
    print '<vmstate><version> version: %x </version>\n<ram>' %version
    i=1
    try:
        while (i<90000): # 5+1+s+8=14+s   TODO; Here hardcoded to 9000 , need to make it generic
            sec_type,section_id = struct.unpack('>bI', f.read(5))
            if ((sec_type == 0x1) or (sec_type == 0x4)): # sec start or full
                len = qemu_get_byte()
                idstr,instance_id,version = struct.unpack(">"+str(len)+"sii", f.read(len+8))
                #print ":%s: instance id: %x  verson: %x  sec_type:%d -------- file offset: %d" %(idstr,instance_id,version,sec_type,f.tell())
                if (idstr == "ram"):
                    read_mem()
                else:
                    if (first_device == 1):
                        first_device = 0
                        mem_file.write(" 0 0 0 \n")
                        print '</ram>'
                    read_device(idstr,version)
                    
                
            elif ((sec_type == 0x2) or (sec_type == 0x3)): #section part or section end
                read_mem()
            elif (sec_type == 0x0):
                print " Completed endoffile:%d sofarread:%d "%(os.fstat(f.fileno()).st_size,f.tell())
                return
            else:
                print "<error> ERROR sec_type:</error>",sec_type
                print "</vmstate>"
                sys.exit(2)
                i=i+1
    except struct.error:
        print "<error> file overrun or underrun: </error>",f.tell()
        print "</vmstate>"
        return ;
