#! /usr/bin/python3
# Import Modules
import paho.mqtt.client as mqtt
import time
from bluepy import btle
from gattlib import *
import function
from configure import *

# Assign Variables
# TCP_ADDRESS = None
# PORT = "1883"
# TOPIC = None
# INTERVAL = None
# BLE_NAME = None
# BLE_ADDRESS = None
# CHAR_UUID = None


def main():
    client = mqtt.Client()
    device_cfg = Config()

    # Get bluetooth address if it doesn't exist yet
    if not device_cfg.has_settings:
        # Scans for BLE Device For INTERVAL seconds
        device_cfg.settings["SCAN_INTERVAL"] = input("Enter BLE scaning time in secods: ")
        device_cfg.settings["BLE_NAME"] = input("Enter Device Name: ")
        device_cfg.settings["BLE_ADDRESS"] = function.scan(int(device_cfg.settings["SCAN_INTERVAL"]), device_cfg.settings["BLE_NAME"])

    # Establish Connection with BLE Device either way
    GATTRequester(device_cfg.settings["BLE_ADDRESS"], False)
    time.sleep(3)  # has to wait for connection, or it'll crash

    # if settings aren't there, setup the rest manually
    if not device_cfg.has_settings:
        device_cfg.settings["CHARACTERISTIC"] = function.choose_CharUUID(device_cfg.settings["BLE_ADDRESS"], device_cfg.settings["BLE_NAME"])
        device_cfg.settings["TCP"] = input("Enter TCP Address for Broker: ")
        device_cfg.settings["PORT"] = input("Enter TCP Port for Broker: ")
        device_cfg.settings["TOPIC"] = input("Enter topic to publish: ")
        device_cfg.settings["PUB_INTERVAL"] = input("Publish every ____ seconds: ")

    # User Input for Establishing Connection with broker
    # TCP_ADDRESS = raw_input("Enter TCP Address for Broker: ")
    # TOPIC = raw_input("Enter topic to publish: ")
    # INTERVAL = int(raw_input("Publish every ____ seconds: "))

    # Establish Connection with Broker
    client.connect(device_cfg.settings["TCP"], int(device_cfg.settings["PORT"]))
    client.on_connect = function.on_connect
    time.sleep(3)
    client.loop_start()

    try:
        while True:
            # Publish message every INTERVAL second
            message = function.read(device_cfg.settings["CHAR_UUID"], device_cfg.settings["BLE_ADDRESS"])
            client.publish(device_cfg.settings["TOPIC"], message)
            print("Published: {}".format(message))
            time.sleep(int(device_cfg.settings["PUB_INTERVAL"]))

    # Stop the Program by doing Ctl+c
    except KeyboardInterrupt:
        pass
    client.loop_stop()

    # Disconnects from Broker
    client.disconnect()
    device_cfg.save_cfg()


if __name__ == "__main__":
    main()
