'''
Author: Garyuu
Date:   2016/8/15
Name:   status
Descr.: Save all core status and settings.
'''
import configuration
from dbaccess import DBAccess
from position import Position
from enum import Enum
import rule

class Status:
    def __init__(self, position_size, player_list, rulename):
        config = configuration.Config('status')
        self.stage = config.get('Contest', 'stage')
        self.substage = config.get('Contest', 'substage')
        self.current_wave = config.get('Contest', 'wave')
        self.position_size = position_size
        self.player_list = player_list
        self.rulename = rulename
        self.rule = rule.Rule(self.stage, self.rulename)
        self.check = None
        self.positions = []
        self.machines = []
        self.build_position_list()

    #=====#
    # Set #
    #=====#
    def new_stage(self, stage, substage):
        self.stage = stage
        self.substage = substage
        self.current_wave = 0
        self.rule.load_stage_rule(self.stage, self.rulename)
        self.save_config()

    def set_machine_auto(self):
        idle_machine = self.num_pos + 1
        for i in range(1, self.num_pos+1):
            if self.machines[i] == 0:
                if i in self.machines:
                    self.positions[i].machine = i
                    self.machines[i] = i
                else:
                    self.positions[i].machine = idle_machine
                    self.machines[i] = idle_machine
                    idle_machine += 1

    def set_machine_to_position(self, machine, position, nosave=False):
        try:
            idx = self.machines.index(machine)
            if idx != position:
                print("[Failed] Cannot assgin machine {} to position {}, machine already assigned on position {}.".format(machine, position, idx))
        except:
            self.positions[position].machine = machine
            self.machines[position] = machine
            self.config.set('Preset', str(position), str(machine))

    def set_position_wait(self, position):
        self.positions[position].wait_for_response()
        self.message += 'Wait for position {} to respond.\n'.format(position)
 
    def set_position_Receiving(self, position):
        self.positions[position].change_state('Receiving')

    def set_position_ok(self, position):
        self.positions[position].received_response()
        self.message += '{}: OK!\n'.format(position)

    def set_position_ready(self, position):
        self.positions[position].change_state('Ready')
        self.message += '{}: Ready!\n'.format(position)

    #=========#
    # Methods #
    #=========#
    def build_position_list(self, player_list):
        self.positions = [None]
        self.machines = [None] + [0] * self.position_size
        for i in range(1, self.num_pos+1):
            self.positions.append(Position(i, 0))
            self.machines.append(0)
        for p in self.player_list:
            self.positions[p.position].players.append(p)

    def send_check(self, machine):
        if self.check:
            self.check(machine)

    def save_wave(self, message):
        pos = self.positions[message['position']]
        pos.save_wave(message['tag'], message['score'])
        if pos.all_back(self.current_wave):
            pos.calculate_score(self.rule)
            self.send_check(int(pos.machine))

    def clear(self):
        self.wave = 0
        self.build_position_list()
        self.save_config()

    def next_wave(self):
        self.current_wave += 1
        self.save_config()

    def position_is_ready(self, position):
        return self.positions[position].is_ready()

    def save_config(self):
        config = configuration.Config('status')
        config.set('Contest', 'stage', self.stage)
        config.set('Contest', 'substage', self.substage)
        config.set('Contest', 'wave', self.current_wave)
        with open('status.cfg', 'w') as configfile:
            config.write(configfile)

    def unlink(self, position):
        self.position[position].machine = 0
        self.machines[position] = 0
