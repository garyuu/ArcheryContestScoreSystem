'''
Author: Garyuu
Date:   2016/8/12
Name:   mqtt_client.py
Descr.: A mqtt client module. Auto-connect to server when created.
        Pass an on_message function can receive and do something
        with the new message.
'''
import paho.mqtt.client as mqtt

MQTT_HOST = ''
MQTT_TOPIC = ''

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, message):
    print('Message: ' + message)

def on_publish(client, userdata, mid):
    print('Published message ID = ' + str(mid))

def create(host, topic, on_message_func = on_message, on_publish_func = on_publish):
    global MQTT_HOST
    global MQTT_TOPIC
    MQTT_HOST = host
    MQTT_TOPIC = topic
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message_func
    client.on_publish = on_publish_func
    client.connect(MQTT_Config['host'])
    return client

def publish(client, message):
    client.publish(MQTT_Config['topic'], message)
