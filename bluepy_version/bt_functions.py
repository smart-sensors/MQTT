from bluepy.btle import *

def le_scan(time):
    scanner = Scanner()
    device_list = scanner.scan()

    i = 0
    for d in device_list:
        print("{}: Address = {} ({}), RSSI = {} dB".format(i, d.addr, d.addrType, d.rssi))
        for (adtype, desc, value) in d.getScanData():
            print("   {} = {}   ".format(desc, value))

        i += 1

    device = device_list[input("Select a device: ")]

    return Peripheral(device)


