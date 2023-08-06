import math
import sys
import os
import time
from re import search
from libeasyobv.fileops import *
import libfpga as fpga
import platform

arch=platform.processor()

bin_fnames = []
channel_en = 0

if os.path.exists('config.py'):
    config=__import__('config')
    mem_width = config.mem_width
    traffic_engine_offset = config.traffic_engine_offset
    fpgamem_mapbase = config.fpgamem_mapbase
    fpgamem_offset = config.fpgamem_offset
    if arch == 'x86_64':
        h2c_fpath=config.h2c_fpath
        c2h_fpath=config.c2h_fpath
    elif arch == 'aarch64':
        cdma_offset = config.cdma_offset
        ps_offset = config.ps_offset
        ps_buf_size = config.ps_buf_size
    else:
        print('Architecutre %s is not supported' % arch)
        sys.exit()
else:
    print('can\'t find the configuration file config.py')
    sys.exit()

def program(fnames,iter_cnt):
    global bin_fnames
    global channel_en
    traffic_engine = fpga.axilite(traffic_engine_offset)
    n_channels = traffic_engine.read32(4)
    if len(fnames) > n_channels:
        print('ERROR: there is/are only %d hardware channels but %d source files are provided, exiting!' % (n_channels,len(fnames)))
        sys.exit()
    rd_addrs = []
    rd_sizes = []
    flitcnts = []
    if len(bin_fnames) == 0:
        for i in range(len(fnames)):
            fname = fnames[i]
            bin_fname = gen_binary(fname,mem_width,bin_fname_user=None,overwrite=False,channel_idx=i)
            if bin_fname == True:
                sys.exit()
            bin_fnames.append(bin_fname)
    if iter_cnt == 0:
        if arch == 'x86_64':
            fpgamem = fpga.fpgamem(h2c_fpath,c2h_fpath,fpgamem_mapbase)
        else:
            fpgamem = fpga.fpgamem(cdma_offset,ps_offset,ps_buf_size,fpgamem_mapbase)
        #write fpgamem
        rd_addr = fpgamem_offset
        for i in range(len(bin_fnames)):
            bin_fname = bin_fnames[i]
            if bin_fname == '-':
                rd_addrs.append(-1)
                rd_sizes.append(-1)
                flitcnts.append(-1)
                print('skiping channel %d' % i)
                continue
            channel_en += 1 << i
            bin_fd = open(bin_fname,'rb')
            print('preparing traffic for channel %d' % i)
            rd_size = int.from_bytes(bin_fd.read(8),sys.byteorder)
            flitcnt = int.from_bytes(bin_fd.read(8),sys.byteorder)
            rd_addrs.append(rd_addr)
            rd_sizes.append(rd_size)
            flitcnts.append(flitcnt)
            fpgamem.file2mem(bin_fd,rd_addr,rd_size)
            rd_addr += (int((rd_size-1)/4096)+1)*4096
            bin_fd.close()
            print('done generating traffic for channel %d' % i)
    print('start injecting traffic')
    timecnt = 0
    while traffic_engine.read32(0) == 0:
        timecnt += 1
        time.sleep(0.01)
        if timecnt == 500:
            print('ERROR: traffic engine time out!')
            sys.exit()
    traffic_engine.write32(0,12)
    for i in range(len(rd_addrs)):
        rd_addr = rd_addrs[i]
        rd_size = rd_sizes[i]
        flitcnt = flitcnts[i]
        if rd_addr == -1:
            continue
        traffic_engine.write64(rd_addr+fpgamem_mapbase,16+24*i)
        traffic_engine.write64(rd_size,24+24*i)
        traffic_engine.write64(flitcnt,32+24*i)
    traffic_engine.write32(1,8)
    traffic_engine.write32(channel_en,12)
    while traffic_engine.read32(0) == 0:
        timecnt += 1
        time.sleep(0.01)
        if timecnt == 500:
            print('ERROR: traffic engine time out!')
            sys.exit()
    print('test finished!')
