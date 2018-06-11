#Import Modules
import paho.mqtt.client as mqtt
import function_mqtt
from time import sleep

#Assign Variables
client = mqtt.Client()
TCP_ADDRESS = "128.10.3.51"
PORT = "1883"
TOPIC = "test"
MESSAGE = "this is a test"
INTERVAL = 1

print("To Start Connection Press 1")
choice = raw_input("Input: ")

if choice == "1":
    #Callback for Connection
    client.on_connect = function_mqtt.on_connect
    #Establish Connection with Broker
    client.connect(TCP_ADDRESS,PORT)

    client.loop_start()
    #Waits until it is connected to broker
    sleep(1)
    print("Press 1 to start publishing message")
    print("Press 2 to start subscribing to message")
    choice = raw_input("Input: ")
    if choice == "1":
            try:
                while True:
                    #Publish message every INTERVAL second
                    client.publish(TOPIC,MESSAGE)
                    print("Published: %s" % MESSAGE)
                    sleep(INTERVAL)
            #Stop the Program by doing Ctl+c
            except KeyboardInterrupt:
                pass
    client.loop_stop()

    #Disconnects from Broker
    client.disconnect()
