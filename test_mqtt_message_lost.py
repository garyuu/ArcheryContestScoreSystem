from mqtt_client import MQTTClient
import threading

config = {
    'host': "broker.hivemq.com",
    'subscribetopic': "/test/asub",
    'publishtopic': "/test/apub",
}

def on_message(client, userdata, message):
    print("Received"+message.payload.decode("utf-8"))
    a = 0
    while(a<100000000):
        a += 1
    print("END"+message.payload.decode("utf-8"))

client = MQTTClient(config)
client.on_message = on_message
client.connect()

while(True):
    str = input("-->")
    client.publish(str)
