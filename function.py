from gattlib import*
from bluepy import btle
# import paho.mqtt.client as mqtt
# import sys
import time
import deserialize as ds

# client = mqtt.Client()


def scan(scan_interval, ble_name):

    #Scans for available BLE device given the BLE device name and it returns
    #the address of the given BLE device if it is detected

    services = DiscoveryService("hci0")
    devices = services.discover(scan_interval)

    for address, name in devices.items():
        print("{} -- []".format(address, name))
        if name == ble_name:
            print("Device Found!")
            return address

    if not ble_name:
        print("Error: Device not found")

# class Connect(object):
#
#     #Establishes BLE connection with the given Address
#
#     def __init__(self, address):
#         self.requester = GATTRequester(address, False)
#         #self.connect()
#     def connect(self):
#         print("Connecting...")
#         sys.stdout.flush()
#         time.sleep(6)
#         self.requester.connect(True)
#         print("Connected")


def choose_CharUUID(address, name):
    # initialize variables

    serviceList=[]
    charList=[]
    serviceChoice = 0
    charChoice = 0
    device = btle.Peripheral(address)

    print("")
    print("Discovered Services in {}: ".format(name))
    print("")

    # Displays all services and stores them in an array called serviceList
    for svc in device.services:
        serviceChoice = serviceChoice + 1
        serviceList.append(str(svc.uuid))
        print ("%d. " % (serviceChoice) + str(svc))
    print("")
    # Allows user to choose the service that they want to see Characteristic of
    serviceChoice = int(input("Choose Service: "))

    # Sets up to see the contents of the choosen service
    userService = btle.UUID(serviceList[serviceChoice-1])
    serviceContent = device.getServiceByUUID(userService)
    print("")
    print("Discovered Characteristics in Service #%d" % (serviceChoice))
    print("")

    # Displays all possible charactertistic of a choosen service
    for ch in serviceContent.getCharacteristics():
        charChoice = charChoice + 1.
        charList.append(str(ch.uuid))
        print ("%d. " % (charChoice) + str(ch.uuid))
    print ("")
    charChoice = int(input("Choose Characteristic: "))

    # disconnects from the device
    device.disconnect()

    # returns the charactertistic uuid
    return charList[charChoice - 1]


def read(charUUID, address):

    #Reads the value of a given charactertistic uuid

    request = GATTRequester(address)
    time.sleep(3)
    text = request.read_by_uuid(charUUID)[0]

    # NEEDS FIXING
    print(text)
    data_tuple = ds.deserialize(text)
    print(data_tuple)
    if data_tuple[0] == "VMM":
        return ds.voltmeter2string(data_tuple)
    else:
        return text


def on_connect(client, userdata, flags, rc):

    # define callback
    if rc == 0:
        print("Connection to Broker Successful")
