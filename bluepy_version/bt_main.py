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
    device = bt_functions.le_scan()
    for i in device.getServices().items():
        print("{} -- {}".format(i[0], i[1]))



if __name__ == "__main__":
    main()