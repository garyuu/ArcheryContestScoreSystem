"""
Author: Garyuu
Date:   2016/8/12
Name:   mqtt_client.py
Descr.: A mqtt client module. Auto-connect to server when created.
        Pass an on_message function can receive and do something
        with the new message.
"""
import paho.mqtt.client as mqtt
import threading

def cnt_f(client, userdata, flags, rc):
    client.subscribe(client.subscribe_topic)

def msg_f(client, userdata, message):
    print('Message: ' + message.payload.decode("utf-8"))

def pub_f(client, userdata, mid):
    print('Published message ID = ' + str(mid))

class MQTTClient(mqtt.Client):
    def __init__(self, host, to_subscribe, to_publish):
        super(MQTTClient, self).__init__()
        self.host = host
        self.subscribe_topic = to_subscribe
        self.publish_topic = to_publish
        self.on_connect = cnt_f
        self.on_message = msg_f
        self.on_publish = pub_f

    def connect(self):
        super(MQTTClient, self).connect(self.host)
        self.start_loop()

    def disconnect(self):
        super(MQTTClient, self).disconnect()
        self.thread.join()

    def publish(self, message):
        super(MQTTClient, self).publish(self.publish_topic, message)

    def start_loop(self):
        self.thread = threading.Thread(target=self.loop_forever)
        self.thread.start()

def main():
    from configuration import SectionConfig
    config = SectionConfig('settings', 'MQTT')
    c = MQTTClient(config['host'],config['subscribetopic'],config['publishtopic'])
    c.connect()
    a = input("-->")
    c.publish(a)
    c.disconnect()
    

if __name__ == "__main__":
    main()
