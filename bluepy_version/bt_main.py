#! /usr/bin/python3

# Library imports
import os
import time
import paho.mqtt.client as mqtt
from bluepy.btle import *

# Local imports
from configure import Config
import deserialize as ds
import bt_functions
# import mqtt_interface


def main():
    TCP = "128.10.3.51"
    PORT = 1883
    
    
    device = bt_functions.le_scan(5)
    characteristic = bt_functions.selectService(device)
    
    client = mqtt.Client("", True, None, mqtt.MQTTv311)
    print(client)
    client.on_connect = on_connect
    client.connect(TCP, PORT)
    client.loop_start()
    time.sleep(1)
    
    try:
        while True:
            raw = characteristic.read()
            message = ds.voltmeter2string(ds.deserialize(raw))
            client.publish("TEST", message)
            print("Published {} to topic {}".format(message, "TEST"))
            time.sleep(3)
    except KeyboardInterrupt:
        pass
    
    #client = mqtt_interface.MQTTConnection(device, characteristic, "TEST", TCP, PORT)
    #try:
    #    client.run(3)
    #except KeyboardInterrupt:
    #    device.disconnect()
    
def on_connect(client, userdata, flags, rc):
    print("Connected to broker")


if __name__ == "__main__":
    main()
