'''
Author: Garyuu
Date:   2016/8/15
Name:   controller
Descr.: The core of the program. It's a bridge to most components.
        A thread create while initializing to handle mqtt loop.
'''
import configuration
import mqtt_client as mqtt
import message_parser as parser
import message_generator as generator
import status
import threading


def reset(position):
    msg = {
        'mode': '0',
        'wave': '0',
    }

    if position != 'all':
        machinesList = [stat.getMachineByPosition(position)]
    else:
        machinesList = stat.getMachinesList()

    for machine in machinesList:
        msg['target'] = machine
        mqtt.publish(client, generator.gen(msg))

def hello(position):
    msg = {
        'mode': '0',
        'wave': '1',
    }

    if position != 'all':
        machinesList = [stat.getMachineByPosition(position)]
    else:
        machinesList = stat.getMachinesList()

    for machine in machinesList:
        msg['target'] = machine
        mqtt.publish(client, generator.gen(msg))

def display_status():
    stat.display_all()

def assign(position, machine):
    stat.setMachineToPosition(machine, positon)

def set(position, data):
    msg = {
        'target'        : stat.getMachineByPosition(position)
        'mode'          : str(stat.getMode())
        'wave'          : str(stat.getWave())
        'position'      : position
        'num_players'   : stat.getNumberOfPlayersOfPosition(position)
        'score'         : []
    }

    for player in stat.getPlayersList():
        msg['score'].append(str(stat.getScore(player)))
    mqtt.publish(client, generator.gen(msg))

def setrule(rulename):
    stat.loadRule(rulename)

def mqtt_on_message(client, userdata, message):
    process(parser.parse(message.payload))

def mqtt_thread_func(client):
    client.loop_forever()

def initialize():
    global stat, client
    stat = status.Status()
    client = MQTT.create(Config.get('MQTT',host), Config.get('MQTT', topic), mqtt_on_message)
    mqtt_thread = threading.Thread(target=mqtt_thread_func, args=(client,))
    mqtt_thread.start()
    mqtt_thread.join()
