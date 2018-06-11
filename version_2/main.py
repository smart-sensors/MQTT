#Import Modules
import paho.mqtt.client as mqtt
import function
import time
from bluepy import btle

#Assign Variables
TCP_ADDRESS = None
PORT = "1883"
TOPIC = None
INTERVAL = None
BLE_NAME = None
BLE_ADDRESS = None
CHAR_UUID = None

client = mqtt.Client()

#Scans for BLE Device For INTERVAL seconds
INTERVAL = int(raw_input("Enter BLE scaning time in secods: "))
BLE_NAME = raw_input("Enter Device Name: ")
BLE_ADDRESS = function.scan(INTERVAL,BLE_NAME)

#Establish Connection with BLE Device
function.Connect(BLE_ADDRESS)

#Allows user to choose getCharacteristics
CHAR_UUID = function.choose_CharUUID(BLE_ADDRESS,BLE_NAME)

#User Input for Establishing Connection with broker
TCP_ADDRESS = raw_input("Enter TCP Address for Broker: ")
TOPIC = raw_input("Enter topic to publish: ")
INTERVAL = int(raw_input("Publish every ____ seconds: "))

#Establish Connection with Broker
client.connect(TCP_ADDRESS,PORT)
client.on_connect = function.on_connect
time.sleep(3)
client.loop_start()
try:
    while True:
        #Publish message every INTERVAL second
        MESSAGE = function.read(CHAR_UUID,BLE_ADDRESS)
        client.publish(TOPIC,MESSAGE)
        print("Published: %s" % MESSAGE)
        time.sleep(INTERVAL)
#Stop the Program by doing Ctl+c
except KeyboardInterrupt:
    pass
client.loop_stop()

#Disconnects from Broker
client.disconnect()
