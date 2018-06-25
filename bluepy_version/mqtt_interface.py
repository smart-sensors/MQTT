import time

import paho.mqtt.client as mqtt
import deserialize as ds

class MQTTConnection():
    def __init__(self, device, characteristic, topic, TCP, PORT):
        super().__init__()
        # private variables
        self.value = None
        self.device = device
        self.characteristic = characteristic
        self.topic = topic
        self.client = mqtt.Client()
        
        print("Here")
        
        # startup functions
        
        self.client.on_connect = self.mqtt_connect
        print("Calling connect...")
        self.client.connect(TCP)
        time.sleep(3)
        self.client.loop_start()
    
    def update(self):
        raw = self.characteristic.read()
        message = ds.voltmeter2string(ds.deserialize(raw))
        self.client.publish(self.topic, message)
        print("Published {} to topic {}".format(message, self.topic))
    
    def run(self, interval):
        while True:
            self.update()
            time.sleep(interval)
            
    def mqtt_connect(client, userdata, flags, rc):
        print("In callback")
        if rc == 0:
            print("Connection to Broker Successful")
        else:
            print("Failed.")
                

if __name__ == "__main__":
    MQTTConnection(None, None, "Test", "128.10.3.51", 1883)