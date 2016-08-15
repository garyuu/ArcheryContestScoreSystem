'''
Author: Garyuu
Date:   2016/8/12
Name:   mqtt_client.py
Descr.: A mqtt client module. Auto-connect to server when created.
        Pass an on_message function can receive and do something
        with the new message.
'''
import paho.mqtt.client as mqtt
import configuration

MQTT_Config = configuration.SectionConfig('settings', 'MQTT')

def setting(option):
    return MQTT_Config.get('Connection', option)

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_Config['subscribetopic'])

def on_message(client, userdata, message):
    print('Message: ' + message)

def on_publish(client, userdata, mid):
    print('Published message ID = ' + str(mid))

def create(on_message_func = on_message, on_publish_func = on_publish):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message_func
    client.on_publish = on_publish_func
    client.connect(MQTT_Config['host'])
    return client

def publish(client, message):
    client.publish(MQTT_Config['publishtopic'])
