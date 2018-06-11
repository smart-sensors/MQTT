#Import Modules
import paho.mqtt.client as mqtt

client = mqtt.Client()

def on_connect(client,userdata,flags,rc):
    #define callback
    if rc == 0:
        print("Connection Successful")
