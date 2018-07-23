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
    device = Peripheral(addr)
    sensor = [x for x in device.getCharacteristics() if x.uuid.getCommonName() == "ff01"][0]
    data = sensor.read()
    device.disconnect()
    fixed = deserialize(data)
    return fixed

def deserialize(bitstream):

    # rebuild data by reversing 'endianness'
    val = 0
    cnt = 0
    
    for x in data_bytes:
        val |= x << (cnt * 8)
        cnt += 1

    # convert to tuple
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