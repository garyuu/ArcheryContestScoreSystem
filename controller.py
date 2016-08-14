import configuration
import mqtt_client as mqtt
import message_parser as parser
import message_generator as generator
import status
import threading


def hello(position):
    msg = {}
    msg['mode'] = 0
    msg['wave'] = 1

    if position != 'all':
        machineList = stat.getMachineByPosition(position)
    else:
        machineList = stat.getMachineList()

    for machine in machineList:
        msg['target'] = machine    
        mqtt.publish(stat, generator.gen(msg))

def display_status():


def assign(position, machine):


def set(position, data):


def setrule(rulename):


def mqtt_on_message(client, userdata, message):
    process(parser.parse(message.payload))

def mqtt_thread_func(client):
    client.loop_forever()

stat = status.Status()

client = MQTT.create(Config.get('MQTT',host), Config.get('MQTT', topic), mqtt_on_message)
mqtt_thread = threading.Thread(target=mqtt_thread_func, args=(client,))
mqtt_thread.start()
mqtt_thread.join()
