def on_connect(client,userdata,flags,rc):
    #define callback
    if rc == 0:
        print("Connection to Broker Successful")

    #Subscribe to Topics
    client.subscribe("Raspberrypi1")
    client.subscribe("Raspberrypi1/setup")
    client.subscribe("Raspberrypi1/setup/DeviceName")
    client.subscribe("Raspberrypi1/subscribe_topic")
