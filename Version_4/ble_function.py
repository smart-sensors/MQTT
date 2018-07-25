from bluepy.btle import *

# NOT NEEDED
import binascii
import struct
import paho.mqtt.client as mqtt
import mqtt_function
import time

def le_scan(time,name):
    scanner = Scanner()
    device_list = scanner.scan()
    for d in device_list:
        for (adtype,desc,value) in d.getScanData():
            if value == name:
                return d.addr

def le_read(addr):
    try:
        device = Peripheral(addr)
    except BTLEException:
        fixed = "CONNECTION FAILURE"
    else:
        sensor = [x for x in device.getCharacteristics() if x.uuid.getCommonName() == "ff01"][0]
        data = sensor.read()
        device.disconnect()
        fixed = deserialize(data)
    
    print("{}".format(fixed))
        
    return fixed

def deserialize(bitstream):
    print(bitstream)
    # rebuild data by reversing 'endianness'
    valhigh = 0
    vallow = 0
    low = bitstream[0:4]
    high = bitstream[4:]
    
    for x in range(0, 4):
        valhigh += high[x]
        vallow += low[x]
    
    val = str(valhigh) + "," + str(vallow)
    
    return val


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("128.10.3.50", 1883)
    client.on_connect = mqtt_function.on_connect
    client.loop_start()
    while True:
        time.sleep(3)
        addr = le_scan(1, "VOLTMETER_ESP32")
        client.publish("test", le_read(addr))
        print("published.")
    client.loop_stop()