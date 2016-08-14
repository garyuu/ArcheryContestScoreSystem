import configuration as Config
import mqtt_client as MQTT
import message_parser as Parser
import message_generator as Generator
import status as Status
import threading

def send_message(command):

def edit_config(command):
    return 0

def process(command):
    return CommandType[command[0]](command)

CommandType = {
    'Message' : send_message,
    'Config'  : edit_config,
}

def mqtt_on_message(client, userdata, message):
    process(Parser.parse(message.payload))

def mqtt_thread_func(client):
    client.loop_forever()

client = MQTT.create(Config.get('MQTT',host), Config.get('MQTT', topic), mqtt_on_message)
mqtt_thread = threading.Thread(target=mqtt_thread_func, args=(client,))
mqtt_thread.start()
mqtt_thread.join()
