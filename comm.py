import RPi.GPIO as RPIO
from PIL import Image
import time
import sys
import logging

from consts import *

def hexf(v):
    return '{:02x}'.format(v)

class VarHeader:
    def __init__(self,size=0,type1=0,name='',version=0,type2=0):
        self.size = size
        self.type1,self.type2 = type1,type2
        self.name = name
        self.version = version
    
    def array(self):
        arr = []
        arr.extend([self.size & 0xFF,(self.size >> 8) & 0xFF])
        arr.append(self.type1)
        #TODO: support names
        name_token = [0]*8
        for i in range(8):
            if i < len(self.name):
                name_token[i] = ord(self.name[i])
        arr.extend(name_token)
        arr.append(self.version)
        arr.append(self.type2)
        
        return arr

    def from_data(self,data):
        self.type1 = data[2]
        
        if self.type1 == VAR_BACKUP:
            self.size1 = little_endian(data[0:1])
            self.size2 = little_endian(data[3:4])
            self.size3 = little_endian(data[5:6])
            self.start = little_endian(data[7:8])
        elif self.type1 in (VAR_FLASH_APP, VAR_FLASH_OS):
            pass
        else:
            self.size = data[0] + (data[1] << 8)
            self.name = ''
            for i in range(3,3+8):
                if not data[i]:
                    break
                self.name += chr(data[i])
            self.version = data[-2]
            self.type2 = data[-1]

        return self

class FlashHeader:
    def __init__(self,data):
        self.size = little_endian((data[0],data[1],data[3],data[4]))
        print(little_endian(data[0:1]))
        print(little_endian(data[3:4]))
        self.type1 = data[2]
        self.flag = data[5]
        self.offset = little_endian(data[6:7])
        self.page = little_endian(data[8:9])

class Packet():
    def __init__(self):
        self.id = 0
        self.cmd_id = 0
        self.data_len = 0
        self.data = []
        self.checksum = 0
        self.checksum_input = 0
        self.checksum_error = False
        
    def echo(self):
        print(hexf(self.id),hexf(self.cmd_id),self.data_len,self.data,hexf(self.checksum))

class Comm:
    def __init__(self,pins):
        self.pins = pins
        self.machine_id = 0x23

        RPIO.setmode(RPIO.BCM)
        for p in pins:
            RPIO.setup(p, RPIO.IN, pull_up_down=RPIO.PUD_UP)
    def read_bit(self):
        value = "null"
        if not RPIO.input(self.pins[0]):
            value = 0
        if not RPIO.input(self.pins[1]):
            if value == 0:
                value = "invalid"
            else:
                value = 1
                
        if type(value) is str:
            return value
        
        #TODO: Replace read response with thread?
        # ACK bit
        RPIO.setup(self.pins[not value], RPIO.OUT)
        RPIO.output(self.pins[not value], False)
        
        # Wait for calc to return
        while not RPIO.input(self.pins[value]): 
            pass
        
        RPIO.output(self.pins[not value], True)
        RPIO.setup(self.pins[not value], RPIO.IN, pull_up_down=RPIO.PUD_UP)
        
        return value
        
    def read_byte(self,count = 1):
        value = 0
        for i in range(8):
            has_read = False
            while not has_read:
                b = self.read_bit()
                if type(b) is int:
                    value += b << i
                    has_read = True
                else:
                    #print(b)
                    pass
        
        return value
        
    def write_bit(self,value):
        RPIO.setup(self.pins[value], RPIO.OUT)
        RPIO.output(self.pins[value], False)
        
        # Wait for calc to return
        while RPIO.input(self.pins[not value]): 
            pass
        
        RPIO.output(self.pins[value], True)
        RPIO.setup(self.pins[value], RPIO.IN, pull_up_down=RPIO.PUD_UP)
        
        while not RPIO.input(self.pins[not value]): 
            pass
            
    def write_byte(self,value):
        for i in range(8):
            self.write_bit((value >> i) & 1)

    def read_packet(self):
        pack = Packet()
        msg = []
        for i in range(4):
            msg.append(self.read_byte())
            
        pack.id = msg[0]
        pack.cmd_id = msg[1]
        pack.data_len = msg[2] + (msg[3] << 8)
        
        #   pack.echo()
        if pack.cmd_id in (0x06,0x15,0x36,0x88,0xA2,0xc9):
            pack.checksum_input = 0
            for i in range(pack.data_len):
                if pack.cmd_id == CMD_DATA:
                    sys.stdout.write(f"\rReceiving...  {i+1}\\{pack.data_len}")
                    if i == pack.data_len -1:
                        sys.stdout.write("\n")
                    sys.stdout.flush()

                byt = self.read_byte()
                pack.data.append(byt)
                pack.checksum_input += byt
            pack.checksum_input = pack.checksum_input & 0xFFFF 
            # get calc checksum
            for i in range(2):
                pack.checksum += self.read_byte() << (i*8)
            
            if pack.checksum_input != pack.checksum:
                pack.checksum_error = True
        
        #print(f"r {pack.cmd_id}")
        return pack

    def write_packet(self,cmd,data=[]):
        self.write_byte(self.machine_id)
        self.write_byte(cmd)
        l = len(data) & 0xFFFF
        self.write_byte(l & 0xFF)
        self.write_byte((l >> 8) & 0xFF)
        if l > 0:
            checksum = 0
            for b in data:
                self.write_byte(b)
                checksum += b
            self.write_byte(checksum & 0xFF)
            self.write_byte((checksum >> 8) & 0xFF)
                
    def poll(self):
        left,right = RPIO.input(self.pins[0]), RPIO.input(self.pins[1])
        if left and right:
            return False
        if not left and not right:
            return False

        return True

def byte16(value):
    l = value & 0xFF
    h = (value & 0xFF00) >> 8
    return bytes((l,h))
    
def bytestr(string, padding):
    out = []
    for i in range(padding):
        if i >= len(string):
            out.append(0)
        else:
            out.append(ord(string[i]))
    return bytes(out)

def little_endian(arr):
    #print(arr)
    value = 0
    for i,v in enumerate(arr):
        value += v << (8*i)
    return value

# ==================
# Commands
#
def versions(pins):
    c = Comm(pins)
    c.write_packet(CMD_VER)
    
    timeout = 1
    while not c.poll():
        w = 0.1
        timeout -= w
        time.sleep(w)
        if timeout <= 0:
            print("timeout :(")
            return
    
    ack = c.read_packet()    # ACK
    if ack.cmd_id == CMD_ACK:
        c.write_packet(CMD_CTS)
        ack = c.read_packet()    # ACK
        if ack.cmd_id == CMD_ACK:
            ver = c.read_packet()
            print("OS:",f"{ver.data[0]}.{ver.data[1]}")
            print("BIOS:",f"{ver.data[2]}.{ver.data[3]}")
            print("Battery:",f"{ver.data[4]}")
            print("Model:",f"{('83+','83+ SE','84+','84+ SE')[ver.data[5]]}")
            print("Language Code:",f"{hexf(ver.data[6])}{hexf(ver.data[7])}")
            c.write_packet(CMD_ACK)

def screenshot(pins):
    c = Comm(pins)
    c.write_packet(CMD_SCR)

    timeout = 1
    while not c.poll():
        w = 0.1
        timeout -= w
        time.sleep(w)
        if timeout <= 0:
            return

    ack = c.read_packet()    # ACK
    if ack.cmd_id == CMD_ACK:
        scr = c.read_packet()
        if scr.cmd_id == CMD_DATA and scr.data_len == 768 and not scr.checksum_error:
            img = Image.new("1", (96,64), color=1)
            for y in range(64):
                for x,b in enumerate(scr.data[y*12:y*12+12]):
                    for i in range(8):
                        c = (not (b>>(7-i)) & 1,)
                        img.putpixel((x*8+i,y), c) 
            img.show()
            img.save("sreenshot.png")
            print("Saved screenshot.png")

def list_dir(pins):
    c = Comm(pins)
    header = VarHeader(0,VAR_DIR)
    #print(header.array())
    c.write_packet(CMD_REQ,header.array())

    timeout = 1
    while not c.poll():
        w = 0.1
        timeout -= w
        time.sleep(w)
        if timeout <= 0:
            print("timeout!")
            return
    ack = c.read_packet()    # ACK
    if ack.cmd_id != CMD_ACK:
        return
    
    free_mem = c.read_packet()
    if free_mem.cmd_id != CMD_DATA:
        return
    
    print(f"Free RAM: {free_mem.data[0] + (free_mem.data[1] << 8)} bytes")
    c.write_packet(CMD_ACK)

    over = False
    # Receive packs
    while not over:
        pack = c.read_packet()
        if pack.cmd_id == CMD_EOT:
            over = True
        elif pack.cmd_id == CMD_VAR:
            header = VarHeader().from_data(pack.data)
            print(f"'{header.name}{VAR_EXT[header.type1]}' ({VAR_DESC[header.type1]}) {header.size} bytes")
            c.write_packet(CMD_ACK)
    
    c.write_packet(CMD_ACK)

def receive(pins, message="receive"):
    c = Comm(pins)
    timeout = 10
    while not c.poll():
        w = 0.1
        timeout -= w
        time.sleep(w)
        if timeout <= 0:
            return

    # Handle Ready
    start = c.read_packet()
    while start.cmd_id == CMD_RDY:
        c.write_packet(CMD_ACK)
        start = c.read_packet()
    c.write_packet(CMD_ACK)    
    if start.cmd_id != CMD_VAR:
        logging.error(f"not a var {hex(start.cmd_id)}")
        return
    count = 0
    while True:
        count += 1

        data = None
        if start.cmd_id == CMD_VAR:
            header = VarHeader().from_data(start.data)
            c.write_packet(CMD_CTS)
            ack = c.read_packet()
            if ack.cmd_id != CMD_ACK:
                return
            data = c.read_packet()
        else:
            data = start

        if data.cmd_id != CMD_DATA:
            return
        
        if not data.checksum_error:
            var_to_file(data.data,
                f"{header.name}{VAR_EXT[header.type1]}"
            )
            c.write_packet(CMD_ACK)
        else:
            logging.error("Invalid Checksum")
            c.write_packet(CMD_ERR)

        if message == "request":
            break
        elif header.type1 == VAR_BACKUP and count == 3:
            break
        else:
            start = c.read_packet()
            if start.cmd_id == CMD_EOT:
                break
            elif start.cmd_id == CMD_VAR:
                c.write_packet(CMD_ACK)
    
    c.write_packet(CMD_ACK)

def request(pins,filename):
    c = Comm(pins)
    name = filename.split(".")[0]
    extension = '.'+filename.split(".")[-1]
    file_type = 0
    for k,v in VAR_EXT.items():
        if v == extension:
            file_type = k
            break
    
    header = VarHeader(0,file_type,name=name)
    #print(header.array())
    c.write_packet(CMD_REQ,header.array())

    timeout = 1
    while not c.poll():
        w = 0.1
        timeout -= w
        time.sleep(w)
        if timeout <= 0:
            return
    ack = c.read_packet()    # ACK
    if ack.cmd_id != CMD_ACK:
        return

    receive(pins, message="request")
    
def backup(pins):
    c = Comm(pins)
    header = VarHeader(0,VAR_BACKUP)
    #print(header.array())
    c.write_packet(CMD_REQ,header.array())
    
    timeout = 1
    while not c.poll():
        w = 0.1
        timeout -= w
        time.sleep(w)
        if timeout <= 0:
            return False

    ack = c.read_packet()    # ACK
    if ack.cmd_id != CMD_ACK:
        return
    receive(pins)
    return
    ack = c.read_packet()    # <ACK
    if ack.cmd_id != CMD_ACK:
        return False
    var = c.read_packet()
    if var.cmd_id != CMD_VAR:
        return False
    
    c.write_packet(CMD_ACK)
    c.write_packet(CMD_CTS)
    
    ack = c.read_packet()    # <ACK
    if ack.cmd_id != CMD_ACK:
        return False
    
    data = []
    print("getting data...")
    for i in range(3):
        data.extend(c.read_packet().data)
        c.write_packet(CMD_ACK) # >ACK
    
    var_to_file(data,"backup.raw",raw=True)
    return True

def send(pins,filename):
    c = Comm(pins)
    header, data = file_to_var(filename)

def receive_os(pins):
    
    print("aaaaaaaaaaa")
    c = Comm(pins)

    h = c.read_packet()
    print(hex(h.cmd_id))
    c.write_packet(CMD_ACK)
    h = c.read_packet()
    print(hex(h.cmd_id))
    
    """
    #c.write_packet(CMD_REQ,VarHeader(0,VAR_FLASH_APP,name="VoidPack").array())
    c.write_packet(CMD_REQ,VarHeader(0xB,VAR_FLASH_OS,name="").array())
    
    timeout = 1
    while not c.poll():
        w = 0.1
        timeout -= w
        time.sleep(w)
        if timeout <= 0:
            return False

    ack = c.read_packet()    # <ACK
    print(hex(ack.cmd_id))
    h = c.read_packet()
    print(hex(h.cmd_id))
    #header = flashheader(h.data)
    #print(header.page,hex(header.type1))
    """

# ====================
# IO Functions
def var_to_file(data,filename,raw=False):
    name, ext = filename.split(".")
    with open(filename,"wb") as f:
        if raw:
            f.write(bytes(data))
        else:
            # Header
            f.write(bytes("**TI83F*","utf-8"))
            f.write(bytes((0x1A, 0x0A, 0x00)))
            f.write(bytes(([0]*42)))
            f.write(byte16(len(data)+17)) # Length
            
            # Variable entry
            dat_section = bytes()
            dat_section += bytes((0x0d,0x00),)
            dat_section += byte16(len(data))    # Length
            for key, value in VAR_EXT.items():
                if value == "."+ext:
                    dat_section += bytes((key,))    
                    break
                
            dat_section += bytestr(name,8)
            dat_section += bytes((0,)) # Version
            dat_section += bytes((0,)) # Flag
            
            dat_section += byte16(len(data))    # Length copy
            dat_section += bytes((data))
            
            f.write(dat_section)
            # Checksum
            checksum = 0
            for b in dat_section:
                checksum += b
            f.write(byte16(checksum))
    print(f"Saved {repr(filename)}")
    
def file_to_var(filename):
    print(filename)
    with open(filename,"rb") as f:
        dump = list(f.read())
    d_header = dump[0:57]
    d_var = dump[57:-2]
    d_var_data = var[17:]
    
    # Variable Header
    
    # Variable Data
    