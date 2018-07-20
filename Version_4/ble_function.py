from bluepy.btle import *
import binascii
import struct

def le_scan(time,name):
    scanner = Scanner()
    device_list = scanner.scan()
    for d in device_list:
        for (adtype,desc,value) in d.getScanData():
            if value == name:
                return d.addr
