from bluepy.btle import *

def le_scan(time):
    scanner = Scanner()
    device_list = scanner.scan()
    
    MAC_list = []

    i = 0
    for d in device_list:
        print("{}: Address = {} ({}), RSSI = {} dB".format(i, d.addr, d.addrType, d.rssi))
        MAC_list.append(d.addr)
        for (adtype, desc, value) in d.getScanData():
            print("   {} = {}   ".format(desc, value))

        i += 1

    device = MAC_list[int(input("Select a device: "))]

    return Peripheral(device)


def selectService(device):
    
    i = 0
    slist = []
    for service in device.getServices():
        print("{}: {}".format(i, service))
        slist.append(service)
        i += 1
    
    selected_service = slist[int(input("Select a service: "))]
    
    i = 0
    clist = []
    for characteristic in selected_service.getCharacteristics():
        temp = characteristic.propertiesToString()
        if "READ" in temp and "WRITE" in temp:
            print("{}: {}".format(i, characteristic))
            clist.append(characteristic)
            i += 1
    
    return clist[int(input("Select a characteristic: "))]
        
        