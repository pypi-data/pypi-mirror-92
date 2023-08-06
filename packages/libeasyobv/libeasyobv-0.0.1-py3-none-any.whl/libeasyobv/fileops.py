import math
import sys
import os
import time
from re import search

def __get_seg_widths(data_width):
    seg_widths = []
    remain_width = data_width
    while remain_width != 0:
        if 2**(math.ceil(math.log2(remain_width))) == int((remain_width-1)/8+1)*8 or remain_width <= 8:
            seg_widths.append(int((remain_width-1)/8)+1)
            break
        else:
            curr_width = 2**(math.floor(math.log2(remain_width)))
            seg_widths.append(int(curr_width/8))
            remain_width -= curr_width
    return seg_widths

def __get_pack_size(mem_width,unit):
    if mem_width/8 < unit:
        return 1
    else:
        return int(mem_width/8/unit)

def get_raw_bytes(vec_list,data_width,mem_width):
    if len(vec_list) == 0:
        return bytes(0)
    seg_widths = __get_seg_widths(data_width)
    pack_size = __get_pack_size(mem_width,seg_widths[-1])
    n_pack = int((len(vec_list)-1)/pack_size)+1
    if len(vec_list) != n_pack*pack_size:
        vec_list += [0]*(n_pack*pack_size-len(vec_list))
    vec_size = sum(seg_widths)
    bytes_pack = len(vec_list) * [bytearray(vec_size)]
    raw_bytes = bytearray(len(vec_list)*vec_size)
    for i in range(len(vec_list)):
        bytes_pack[i] = vec_list[i].to_bytes(vec_size,sys.byteorder)
    raw_idx=0
    for i in range(n_pack):
        pack_idx = 0
        for seg_width in seg_widths:
            for j in range(pack_size):
                raw_bytes[raw_idx:raw_idx+seg_width] = bytes_pack[i*pack_size+j][pack_idx:pack_idx+seg_width]
                raw_idx += seg_width
            pack_idx += seg_width
    return raw_bytes

class axis_interpreter:
    def __init__(self,csv_name):
        self.idx_sheet = {
            'TDATA':[-1,0],
            'TVALID':[-1,0],
            'TREADY':[-1,0],
            'TKEEP':[-1,0],
            'TLAST':[-1,0],
            'TSTRB':[-1,0],
            'TDEST':[-1,0],
            'TUSER':[-1,0],
            'TID':[-1,0],
            'TIMEOUT':[-1,0],
            'REPEAT':[-1,0]
        }
        self.def_fields = ['TDATA','TVALID','TREADY','TKEEP','TLAST','TSTRB','TDEST','TUSER','TID','TIMEOUT','REPEAT']
        self.total_width = 0
        self.enabled_fields = 0
        self.csv_fd = None
        self.line_num=1
        self.csv_fd = open(csv_name,'r')
    def __parse_header(self):
        header=self.csv_fd.readline().rstrip().split(',')
        DWIDTH = 1
        for def_field in self.def_fields:
            for i in range(len(header)):
                usr_field = header[i]
                if search(def_field,usr_field.upper()):
                    if def_field == "TVALID" or def_field == "TLAST":
                        width = 1
                    elif def_field == "TREADY":
                        width = 2
                    elif def_field == "TKEEP" or  def_field == "TSTRB":
                        width = int(DWIDTH/8)
                    elif search(r'\[.*\]',usr_field):
                        field_width = search(r'\[.*\]',usr_field)
                        idx_low, idx_high = field_width.span()
                        idx_low += 1
                        idx_high -= 1
                        width = int(usr_field[idx_low:idx_high])
                        if def_field == "TDATA":
                            DWIDTH = width
                    else:
                        width = 1
                        if def_field == "TDATA":
                            DWIDTH = 1
                    self.idx_sheet[def_field][0] = i
                    self.idx_sheet[def_field][1] = width
                    self.total_width += width
                    self.enabled_fields += 1
                    break
        if self.idx_sheet['TDATA'][0] == -1:
            print('missing required field TDATA in the first line of the CSV, exiting!')
            return True
        return False
    def __parse_line(self):
        self.line_num += 1
        line = self.csv_fd.readline()
        if not line:
            return -1
        fields = line.rstrip().split(',')
        if len(fields) < self.enabled_fields:
            print("ERROR at line %d: there are %d fields in the csv header, but only got %d this line" % (self.line_num, self.enabled_fields, len(fields)))
            return True
        ret = 0
        shift_bits = 0
        for def_field in self.def_fields:
            idx = self.idx_sheet[def_field][0]
            if idx == -1:
                continue
            field = fields[idx]
            field_width = self.idx_sheet[def_field][1]
            field_max = (1 << field_width) - 1
            if def_field == "TREADY" and field.upper() == 'X':
                field_val = 2
            elif len(field) < 3:
                field_val = int(field)
            elif (field[0:2] == '0x'):
                field_val = int(field,16)
            elif (field[0:2] == '0b'):
                field_val = int(field,2)
            else:
                field_val = int(field)
            if field_val <= field_max: 
                ret += (field_val << shift_bits)
            else:
                print("WARNING at line %d: %s is specified as %d bit in the csv header, but got value %d (%s), replacing it with %d to avoid overflow" % (self.line_num, def_field, field_width, field_val, hex(field_val), field_max))
                ret += (field_max << shift_bits)
            shift_bits += field_width
        return ret    
    def write_bin(self,fname,mem_width):
        if self.__parse_header():
            return True
        bin_fd = open(fname,'wb')
        bin_fd.write(bytes(16))
        total_size = 0
        total_flits = 0
        eof_flag = False
        while not eof_flag:
            vec_list = []
            for _ in range(32*1024**2):
                vec = self.__parse_line()
                if vec == True:
                    os.remove(fname)
                    return True
                if vec == -1:
                    self.csv_fd.close()
                    eof_flag = True
                    break
                else:
                    vec_list.append(vec)
                    total_flits+=1
            if not vec_list:
                break
            raw_bytes = get_raw_bytes(vec_list,self.total_width,mem_width)
            bin_fd.write(raw_bytes)
            total_size += len(raw_bytes)
        bin_fd.seek(0)
        bin_fd.write(total_size.to_bytes(8,sys.byteorder))
        bin_fd.write(total_flits.to_bytes(8,sys.byteorder))
        bin_fd.close()
        return False

class raw_interperter:
    def __init__(self,fname):
        self.raw_fd = open(fname,'r')
        self.datawidth = -1
    def __parse_header(self):
        header=self.raw_fd.readline().rstrip().lower()
        header_match = search(r'datawidth\[.*\]',header)
        if not header_match:
            print("ERROR: wrong raw file format, no datawidth definition at the first line. The first line should be 'datawidth[x]'")
            return True
        width_match = search(r'\[.*\]',header)
        idx_low, idx_high = width_match.span()
        idx_low += 1
        idx_high -= 1
        self.datawidth = int(header[idx_low:idx_high])
        if int(self.datawidth) <= 0:
            print("ERROR: datawidth can't be smaller than 0")
            return True
        return False
    def write_bin(self,fname,mem_width):
        if self.__parse_header():
            return True
        data_width=self.datawidth
        bin_fd = open(fname,'wb')
        bin_fd.write(bytes(16))
        totoal_size = 0
        total_flits = 0
        eof_flag = False
        while not eof_flag:
            vec_list = []
            for _ in range(32*1024**2):
                line = self.raw_fd.readline()
                if line:
                    vec_list += [int(line.rstrip())]
                    total_flits += 1
                else:
                    self.raw_fd.close()
                    eof_flag = True
                    break
            if not vec_list:
                break
            raw_bytes = get_raw_bytes(vec_list,data_width,mem_width)
            bin_fd.write(raw_bytes)
            totoal_size += len(raw_bytes)
        bin_fd.seek(0)
        bin_fd.write(totoal_size.to_bytes(8,sys.byteorder))
        bin_fd.write(total_flits.to_bytes(8,sys.byteorder))
        bin_fd.close()
        return False

def gen_binary(fname,mem_width,bin_fname_user=None,overwrite=False,channel_idx=-1):
    if fname == '-':
        return '-'
    fname_noext, fname_ext = os.path.splitext(fname)
    if fname_ext == '.bin':
        return fname
    if bin_fname_user:
        bin_fname = bin_fname_user
    else:
        bin_fname = fname_noext+'.bin'
    if os.path.exists(bin_fname) and not overwrite:
        bin_mtime = os.stat(bin_fname).st_mtime
        src_mtime = os.stat(fname).st_mtime
        if bin_mtime > src_mtime:
            if channel_idx != -1:
                print('using cached binary file %s for channel %d' % (bin_fname, channel_idx))
            else:
                print('the target binary file is existed and appears to be newer than the source file. not generating the new binary file')
            return bin_fname
    if channel_idx != -1:
        print('generating binary file for channel %d' % (channel_idx))
    else:
        print('generating binary file')
    if fname_ext == '.csv':
        interpreter = axis_interpreter(fname)
        if interpreter.write_bin(bin_fname,mem_width):
            return True
    else:
        interpreter = raw_interperter(fname)
        if interpreter.write_bin(bin_fname,mem_width):
            return True
    if channel_idx != -1:
        print('done generating binary file for channel %d' % (channel_idx))
    else:
        print('done generating binary file')
    return bin_fname
