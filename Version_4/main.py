#! /usr/bin/python3

#Import Libraries
import paho.mqtt.client as mqtt
import time

#Import Local Libraries
import mqtt_function
import ble_function
import save_function

#Assign Variables
TCP_ADDRESS = "XXX.XXX.XXX"
PORT = 1883
client = mqtt.Client()
monitor = {}
BLE_Device_Name = {}

def on_message(client, userdata, message):
    #Creates a global variable dictionary with messsage topic and assosiated message
    global monitor
    topic = str(message.topic)
    print(message.payload)
    message = message.payload.decode('ascii')
    print(message)

    #Checks if message topic is found inside the dictionary
    if topic not in monitor:
        #Apend to dictionary with new message topic and assosiated message
        monitor.update({topic: message})
    else:
        #Updates message topic with new message
        monitor[topic] = message


#Establish connection with broker
client.connect(TCP_ADDRESS,PORT)
client.on_connect = mqtt_function.on_connect
client.on_message = on_message
client.loop_start()

# TEMPORARY DELETE THIS
devlist = []

try:
    while True:
        #Update rate in seconds
        time.sleep(3)
        print(monitor.values())

        #Connect to BLE device
        if ("ble_connect" in monitor.values() and monitor["Raspberrypi2/setup/DeviceName"] != ""):
            print("Made it :)")
            #scans for BLE devices for 3 seconds and attemps to connect with given device name
            ble_address = ble_function.le_scan(3,monitor["Raspberrypi2/setup/DeviceName"])

            #Initilize topic to publish BLE connectivity status
            BLE_Status_topic = "Raspberrypi2/"+monitor["Raspberrypi2/setup/DeviceName"]+"/BLE_Status"

            #Publishes statues of BLE connectivity status
            if ble_address:
                print("Successfully connected")
                client.publish(BLE_Status_topic,"Successfully Connected")
                #Saves BLE Device Name to configuration file
                save_function.write_config("BLE Device Name",monitor["Raspberrypi2/setup/DeviceName"])
                devlist.append(monitor["Raspberrypi2/setup/DeviceName"])
            else:
                client.publish(BLE_Status_topic,"Connection Error")

            monitor["Raspberrypi2/setup/DeviceName"] = ""

        #Sends saved device names
        elif ("saved_device" in monitor.values()):
            names = ""

            #Reads Configuration file for BLE Device Name
            BLE_Device_Name = save_function.read_config("BLE Device Name")

            #Create a long string with all saved device name with spaces in between
            for x in range(0,len(BLE_Device_Name)):
                names = BLE_Device_Name["%i"%x] + " " + names

            #Publishes saved device names
                client.publish("Raspberrypi2/Name_list",names)

        #Reads BLE Device Reading
        elif ("subscribe" in monitor.values()):
            if (monitor["Raspberrypi2/subscribe_topic"] == "Temperature"):
                unit = " F"
            else:
                unit = "";
        # TODO: 1. Determine address of valid characteristic of BLE device
        #       2. Make function that accepts a MAC and uses Peripheral to grab the data from the device
        #       3. Client.publish(topic, data)
        #       4. Timing of data updates
            deviceName = save_function.read_config("BLE Device Name");

            for x in range(0,len(deviceName)):
                device = deviceName["%i"%(x)];
                addr = ble_function.le_scan(1, device);
                if addr == None:
                    client.publish("Raspberrypi2/" + device, "Connection Error")
                else:
                    print("got address")
                    data = ble_function.le_read(addr)
                    client.publish("Raspberrypi2/" + device, str(data) + unit)

except KeyboardInterrupt:
    pass
