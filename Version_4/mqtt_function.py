def on_connect(client,userdata,flags,rc):
    #define callback
    if rc == 0:
        print("Connection to Broker Successful")

    #Subscribe to Topics
    client.subscribe("Raspberrypi2")
    client.subscribe("Raspberrypi2/setup")
    client.subscribe("Raspberrypi2/setup/DeviceName")
    client.subscribe("Raspberrypi2/subscribe_topic")
