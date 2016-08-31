'''
Author: Garyuu
Date:   2016/8/15
Name:   controller
Descr.: The core of the program. It's a bridge to most components.
'''
import configuration
from mqtt_client import MQTTClient
import message_parser as parser
import message_generator as generator
import status
import threading

class Controller:
    def __init__(self):
        self.config = configuration.Config('settings')
        self.load_config()
        self.stage_iter = iter(self.schedule)
        self.current_stage = next(self.stage_iter)

        # Launch MQTT client
        m_conf = configuration.SectionConfig('settings', 'MQTT')
        self.mqtt = MQTTClient(m_conf)
        self.mqtt.on_message = self.mqtt_on_message
        self.mqtt.connect()

        # Launch status
        self.status = status.Status(self.get_total_number_of_position())
        self.status.check = self.all_sent_back_check
        self.status_setstage()
    
    def __del__(self):
        self.destroy()

    #==================#
    # Controll Machine #
    #==================#
    def machine_short_message(self, position, mode):
        msg = {'mode': mode}
        if position != 'all':
            machine_list = [self.status.get_machine_by_position(int(position))]
        else:
            machine_list = self.status.machines

        for machine in machine_list:
            msg['target'] = machine
            self.status.set_position_wait(int(position))
            self.mqtt.publish(generator.gen(msg))

    def machine_reset(self, position):
        self.machine_short_message(position, 'r')

    def machine_hello(self, position):
        self.machine_short_message(position, 'h')

    def machine_force(self, position):
        self.machine_short_message(position, 'f')

    def machine_assign(self, position, machine):
        self.status.set_machine_to_position(int(machine), int(position))

    def machine_assign_auto
        self.status.set_machine_auto()

    def machine_unlink(self, position):
        self.status.unlink(int(position))

    def machine_set(self, position):
        if self.status.position_is_busy(int(position)):
            print("The machine is too busy to receive set messages.")
        else:
            msg = {
                'target'        : self.status.get_machine_by_position(int(position)),
                'mode'          : str(self.status.get_mode),
                'wave'          : str(self.status.get_wave),
                'position'      : position,
                'num_players'   : self.status.get_number_of_players_of_position(int(position)),
                'score'         : [],
            }

            for player in self.status.get_player_list_of_position(int(position)):
                msg['score'].append(str(self.status.get_score(player)))
            self.status.set_wait(int(position))
            self.mqtt.publish(generator.gen(msg))
            self.status.set_position_busy(int(position))
    
    #=================#
    # Controll Status #
    #=================#
    def status_setrule(self, rulename):
        self.status.set_rulename(rulename)

    def status_clear(self):
        self.status.clear()

    def status_nextwave(self):
        self.status.next_wave()

    def status_nextstage(self):
        try:
            self.current_stage = next(self.stage_iter)
        except:
            print("Already in end stage.")

    def status_setstage(self):
            self.status.set_mode(self.current_stage)
            self.status.set_substage('')

    def status_display(self):
        print(self.status)

    #=========#
    # Methods #
    #=========#
    def destroy(self):
        self.mqtt.disconnect()

    def mqtt_on_message(self, client, userdata, message):
        self.message_process(parser.parse(message.payload))

    def message_process(self, message):
        if message['type'] == 'ok':
            self.status.set_position_ok(int(message['position']))
        elif message['type'] == 'ready':
            self.status.set_position_(int(message['position']))
        elif message['type'] == 'wave':
            self.status.save_wave(message)

    def all_sent_back_check(self, machine):
        msg = {'mode': 'g', 'target': str(machine)}
        self.mqtt.publish(generator.gen(msg))

    def load_config(self):
        self.schedule = self.config.get('Contest', 'schedule').split(',')
        self.groups = {}
        groups = self.config.get('Contest', 'groups').split(',')
        for group in groups:
            self.groups[group] = self.config.getint('Group', group)
            
    def get_total_number_of_position(self):
        total = 0
        for group in self.groups:
            total += self.groups[group]
        return total
