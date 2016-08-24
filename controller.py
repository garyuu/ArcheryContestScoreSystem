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
        self.mqtt = MQTTClient(m_conf['host'], m_conf['subscribetopic'], m_conf['publishtopic'])
        self.mqtt.on_message = self.mqtt_on_message
        self.mqtt.connect()

        # Launch status
        self.status = status.Status(self.all_sent_back_check)
    
    def __del__(self):
        self.destroy()

    def destroy(self):
        self.mqtt.disconnect()

    def mqtt_on_message(self, client, userdata, message):
        self.message_process(parser.parse(message.payload))

    def message_process(self, message):
        if message['type'] == 'ok':
            self.status.setPositionOk(int(message['position']))
        elif message['type'] == 'ready':
            self.status.setPositionReady(int(message['position']))
        elif message['type'] == 'wave':
            self.status.saveWave(message)

    def all_sent_back_check(self, machine):
        msg = {'mode': 'g', 'target': machine}
        self.mqtt.publish(generator.gen(msg))

    ##### Controll Machine ####
    def machine_reset(self, position):
        msg = {'mode': 'r'}
        if position != 'all':
            machinesList = [self.status.getMachineByPosition(int(position))]
        else:
            machinesList = self.status.getMachinesList()

        for machine in machinesList:
            msg['target'] = machine
            self.status.setWait(int(position))
            self.mqtt.publish(generator.gen(msg))

    def machine_hello(self, position):
        msg = {'mode': 'h'}
        if position != 'all':
            machinesList = [self.status.getMachineByPosition(int(position))]
        else:
            machinesList = self.status.getMachinesList()

        for machine in machinesList:
            msg['target'] = machine
            self.status.setWait(int(position))
            self.mqtt.publish(generator.gen(msg))

    def machine_force(self, position):
        msg = {'mode': 'f'}
        if position != 'all':
            machinesList = [self.status.getMachineByPosition(int(position))]
        else:
            machinesList = self.status.getMachinesList()

        for machine in machinesList:
            msg['target'] = machine
            self.status.setWait(int(position))
            self.mqtt.publish(generator.gen(msg))

    def machine_assign(self, position, machine):
        self.status.setMachineToPosition(int(machine), int(position))

    def machine_set(self, position):
        if self.status.positionIsBusy(int(position)):
            print("The machine is too busy to receive set messages.")
        else:
            msg = {
                'target'        : self.status.getMachineByPosition(int(position)),
                'mode'          : str(self.status.mode.value),
                'wave'          : str(self.status.wave),
                'position'      : position,
                'num_players'   : self.status.getNumberOfPlayersOfPosition(int(position)),
                'score'         : [],
            }

            for player in self.status.getPlayersListOfPosition(int(position)):
                msg['score'].append(str(self.status.getScore(player)))
            self.status.setWait(int(position))
            self.mqtt.publish(generator.gen(msg))
            self.status.setPositionBusy(int(position))
    
    #### Controll Status ####
    def status_setrule(self, rulename):
        self.status.loadRule(rulename)

    def status_clear(self):
        self.status.clear()

    def status_nextwave(self):
        self.status.nextWave()

    def status_display(self):
        print(self.status)

