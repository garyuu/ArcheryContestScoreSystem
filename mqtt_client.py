import configuration
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe(CONF_TOPIC)

def mqtt_create(host, topic):
    client = mqtt.Client()


