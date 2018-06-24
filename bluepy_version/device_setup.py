#! /usr/bin/python3

import os
import bt_main
import paho.mqtt.client as mqtt
import time

TCP = None
PORT = None



def menu():
    config = Configuration()
    selection = None
    while selection != 1:
        print("Startup menu: ")
        print("1. Run")
        print("2. Setup (do this first!)")
        selection = int(input("Selection: "))
        
        if selection == 2:
            setup_menu(config)

def setup_menu(config):
    selection = None
    while selection != 4:
        print("=====Setup Mode=====")
        print("Select a setup option: \n")
        print("1. View current setup")
        print("2. Edit broker settings")
        print("3. Add/remove ESP32")
        print("4. Return")
        selection = input("Selection: ")
        
        if selection == '1':
            print(config)
        else if selection == '2':
            broker_setup(config)
        else if selection == '3':
            add_device()
        
    
    print("We will now create a configuration file.")
    print("Do not move this file to a different directory,")
    print("or alter it outside of this setup program.")
    
    print("\n\n")
    
    with open("device_setup.cfg", "w") as fp:
        data = []
        data.append("TCP={}\n".format(TCP))
        data.append("PORT={}\n".format(PORT))
        fp.writelines(data)
    
    print("Configuration file created. Returning to menu...")

def broker_setup(config):
    TCP = str(input("Enter the TCP address of the MQTT broker: "))
    PORT = str(input("Enter the port to use for MQTT (default 1883): "))
    
    if not PORT:
        PORT = "1883"
    else:
        PORT = int(PORT)
    
    print("Testing connection...")
    test_client = mqtt.Client("", True, None, mqtt.MQTTv311)
    test_client.on_connect = bt_main.on_connect
    test_client.connect(TCP, PORT)
    test_client.loop_start()
    time.sleep(1)
    test_client.publish("setup", "testing")
    test_client.disconnect()
    
    success = input("Did you see the test message? (y/n)")
    if success == 'y':
        client.add_parameter("TCP", TCP)
        client.add_parameter("PORT", PORT)
        print("Setup complete.")
    else:
        print("Check your TCP/Port and try again later")

class Configuration:
    def __init__(self):
        self.data = {}
        self.has_setup = False
        self.data["DEVICES"] = []
        self.read_cfg()
    
    def __str__(self):
        if self.has_setup:
            return "===Broker===\nTCP: {}\nPort: {}\n===Devices===\n".format(self.data["TCP"], self.data["PORT"]) + "".join(["{}: {}\n".format(name, addr) for name, addr, _ in self.data["DEVICES"]])
        else:
            return "No cfg file found! Please setup your device"
    
    def read_cfg(self):
        if "device_setup.cfg" in os.listdir():
            self.has_setup = True
            with open("device_setup.cfg", "r") as fp:
                raw = fp.readlines()
                key = None
                value = None
                line = 0
                # print(raw)
                while key != "N_DEVICES":
                    key, value = raw[line].split("=")
                    self.data[key] = value.replace("\n", "")
                    line += 1
                    
                for device in raw[line:len(raw)]:
                    name, desc = device.split("=")
                    addr, uuid = desc.split(",")
                    self.data["DEVICES"].append((name, addr, uuid.replace("\n", "")))
                    print(self.data["DEVICES"])
        
    def save(self):
        with open("device_setup.cfg", "w") as fp:
            data = []
            data.append("{}={}".format("TCP", self.data["TCP"]))
            data.append("{}={}".format("PORT", self.data["PORT"]))
            data.append("{}={}".format("N_DEVICES", self.data["N_DEVICES"]))
            
            for name, addr, uuid in self.data["DEVICES"]:
                data.append("{}={},{}".format(name, addr, uuid))
    
    def add_parameter(self, key, value):
        if key == "DEVICES":
            self.data["DEVICES"].append(value)
        else:
            self.data[key] = value
        

if __name__ == "__main__":
    menu()
    bt_main.main(TCP, PORT)