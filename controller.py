'''
Author: Garyuu
Date:   2016/8/15
Name:   controller
Descr.: The core of the program. It's a bridge to most components.
        A thread create while initializing to handle mqtt loop.
'''
import configuration
from mqtt_client import MQTTClient
import message_parser as parser
import message_generator as generator
import status
import threading

class Controller:
    def __init__(self):
        # Launch MQTT client

        m_conf = configuration.SectionConfig('settings', 'MQTT')
        self.mqtt = MQTTClient(mconf['host'], mconf['subscribetopic'], mconf['publishtopic'])
        self.mqtt.on_message = self.mqtt_on_message
        self.mqtt.connect()

        # Launch status
        self.status = status.Status()

    def destroy(self):
        self.mqtt.disconnect()

    def mqtt_on_message(self, client, userdata, message):
        self.message_process(parser.parse(message.payload))

    def message_process(message):
        if message['type'] == 'ok':
            stat.setPositionOk(int(message['position']))
        elif message['type'] == 'wave':
            stat.saveWave(message)

    ##### Controll Machine ####
    def machine_reset(position):
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

    def machine_hello(position):
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

    def machine_assign(position, machine):
        stat.setMachineToPosition(int(machine), int(position))

    def machine_set(position, data):
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
    
    #### Controll Status ####
    def status_setrule(rulename):
        stat.loadRule(rulename)

    def status_clear():
        stat.clear()

    def status_display():
        print(stat)

