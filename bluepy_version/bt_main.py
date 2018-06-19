#! /usr/bin/python3

# Library imports
import os
import paho.mqtt.client as MQTT
from bluepy.btle import *

# Local imports
from configure import Config
import deserialize as ds
import bt_functions


def main():
    device = bt_functions.le_scan(5)
    characteristic = bt_functions.selectService(device)
    a = characteristic.read()
    b = ds.deserialize(a)
    print(ds.voltmeter2string(b))
    print("done")
    device.disconnect()
    



if __name__ == "__main__":
    main()
