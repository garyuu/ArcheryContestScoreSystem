import configuration as config
import paho.mqtt.client as mqtt

MQTT_Config = config.ConfigSectionMap('MQTT')

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_Config['topic'])

#def on_publish(client, userdata, mid):
#    print("published")

def create(on_message):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    #client.on_publish = on_publish
    client.connect(MQTT_Config['host'])
    return client

def publish(client, message):
    client.publish(MQTT_Config['topic'], message)
