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
        'mode': 'r',
    }

    if position != 'all':
        machinesList = [stat.getMachineByPosition(int(position))]
    else:
        machinesList = stat.getMachinesList()

    for machine in machinesList:
        msg['target'] = machine
        stat.setWait(int(position))
        mqtt.publish(client, generator.gen(msg))

def hello(position):
    msg = {
        'mode': 'h',
    }

    if position != 'all':
        machinesList = [stat.getMachineByPosition(int(position))]
    else:
        machinesList = stat.getMachinesList()

    for machine in machinesList:
        msg['target'] = machine
        stat.setWait(int(position))
        mqtt.publish(client, generator.gen(msg))

def display_status():
    print(stat)

def assign(position, machine):
    stat.setMachineToPosition(int(machine), int(positon))

def set(position, data):
    msg = {
        'target'        : stat.getMachineByPosition(int(position)),
        'mode'          : str(stat.mode.value),
        'wave'          : str(stat.wave),
        'position'      : position,
        'num_players'   : stat.getNumberOfPlayersOfPosition(int(position)),
        'score'         : [],
    }

    for player in stat.getPlayersListOfPosition(int(position)):
        msg['score'].append(str(stat.getScore(player)))
    stat.setWait(int(position))
    mqtt.publish(client, generator.gen(msg))

def setrule(rulename):
    stat.loadRule(rulename)

def status_clear():
    stat.clear()

def message_process(message):
    if message['type'] == 'ok':
        stat.setPositionOk(int(message['position']))
    elif message['type'] == 'wave':
        stat.saveWave(message)

def mqtt_on_message(client, userdata, message):
    message_process(parser.parse(message.payload))

def mqtt_thread_func(client):
    client.loop_forever()

def initialize():
    global stat, client
    stat = status.Status()
    client = mqtt.create(mqtt_on_message)
    mqtt_thread = threading.Thread(target=mqtt_thread_func, args=(client,))
    mqtt_thread.start()
    mqtt_thread.join()
