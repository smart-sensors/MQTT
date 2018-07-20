#Import Libraries
import paho.mqtt.client as mqtt
import time

#Import Local Libraries
import mqtt_function
import ble_function
import save_function

#Assign Variables
TCP_ADDRESS = "128.10.3.51"
PORT = "1883"
client = mqtt.Client()
monitor = {}
BLE_Device_Name = {}

def on_message(client, userdata, message):
    #Creates a global variable dictionary with messsage topic and assosiated message
    global monitor
    topic = str(message.topic)
    message = str(message.payload)

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

try:
    while True:
        #Update rate in seconds
        time.sleep(3)

        #Connect to BLE device
        if ("ble_connect" in monitor.values() and monitor["Raspberrypi1/setup/DeviceName"] != ""):

            #scans for BLE devices for 3 seconds and attemps to connect with given device name
            ble_address = ble_function.le_scan(3,monitor["Raspberrypi1/setup/DeviceName"])

            #Initilize topic to publish BLE connectivity status
            BLE_Status_topic = "Raspberrypi1/"+monitor["Raspberrypi1/setup/DeviceName"]+"/BLE_Status"

            #Publishes statues of BLE connectivity status
            if ble_address is not None:
                client.publish(BLE_Status_topic,"Successfully Connected")
                #Saves BLE Device Name to configuration file
                save_function.write_config("BLE Device Name",monitor["Raspberrypi1/setup/DeviceName"])
            else:
                client.publish(BLE_Status_topic,"Connection Error")

        #Sends saved device names
        elif ("saved_device" in monitor.values()):
            names = ""

            #Reads Configuration file for BLE Device Name
            BLE_Device_Name = save_function.read_config("BLE Device Name")

            #Create a long string with all saved device name with spaces in between
            for x in range(0,len(BLE_Device_Name)):
                names = BLE_Device_Name["%i"%x] + " " + names

            #Publishes saved device names
	        client.publish("names",names)

        #Reads BLE Device Reading
        elif ("subscribe" in monitor.values()):
            if (monitor.values["Raspberrypi1/subscribe_topic"] == "Temperature"):
                print "yes"

except KeyboardInterrupt:
    pass
