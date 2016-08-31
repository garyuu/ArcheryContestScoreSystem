'''
Author: Garyuu
Date:   2016/8/15
Name:   status
Descr.: Save all core status and settings.
'''
#from sql_wrapper import SQLWrapper
import configuration
from dbaccess import DBAccess
from position import Position
from enum import Enum

class ModeEnum(Enum):
    Practice        = '1'
    Qualifying      = '1'
    IndividualPoint = '2'
    TeamPoint       = '3'
    IndividualScore = '4'
    TeamScore       = '5'


class Status:
    def __init__(self, num_pos):
        self.config = configuration.Config('status')
        self.num_pos = num_pos
        self.message = ""
        self.check = None
        self.load_rule_wave()
        self.build_position_list()

    def __del__(self):
        self.save_config()

    def __str__(self):
        message = self.message
        message += "=====================================\n"
        message += "Stage: {}-{} Mode{} Wave{} Rule: {}\n".format(
            self.get_stage(), self.get_substage(), self.get_mode(),
            self.get_wave(), self.get_rulename())
        for p in self.positions:
            message += p
        return message

    #=====#
    # Get #
    #=====#
    def get_mode(self):
        return self.config.getint('Contest', 'mode')

    def get_wave(self):
        return self.config.getint('Contest', 'wave')
        
    def get_rulename(self):
        return self.config.get('Contest', 'rulename')

    def get_stage(self):
        return self.config.get('Contest', 'stage')

    def get_substage(self):
        return self.config.get('Contest', 'substage')

    def get_machine_by_position(self, position):
        return self.positions[position].machine

    def get_player_list_of_position(self, position):
        db_msg = {
            'action' = 'playerlistofposition',
            'position' = position,
        }
        return DBAccess.request(db_msg)

    def get_number_of_players_of_position(self, position):
        return len(self.get_player_list_of_position(position))

    def get_score(self, tag, stage=None):
        db_msg = {
            'action' = 'scorearray',
            'tag' = tag,
            'stage' = stage if stage else self.get_stage(),
        }
        score_array = DBAccess.request(db_msg)
        total = 0
        for wave in score_array:
            for i in wave:
                j = int(i)
                if j == 11:
                    total += 10
                elif j >= 0:
                    total += j
        return total

    def get_position_by_player_tag(self, tag):
        for i in range(1, len(self.positions)):
            if tag in self.positions[i].players:
                return i

    #=====#
    # Set #
    #=====#
    def set_mode(self, mode): # mode should be str
        self.config.set('Contest', 'mode', ModeEnum[mode].value)
        self.config.set('Contest', 'stage', mode)
        self.load_rule_wave()
        self.clear()

    def set_wave(self, wave): # wave should be int
        self.config.set('Contest', 'wave', str(wave))

    def set_rulename(self, rulename):
        self.config.set('Contest', 'rulename', rulename)
        self.load_rule_wave(rulename)

    def set_substage(self, substage):
        self.config.set('Contest', 'wave', substage)

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
        self.positions[position].WaitForResponse()
        self.message += 'Wait for position {} to respond.\n'.format(position)
 
    def set_position_busy(self, position):
        self.positions[position].ChangeStateToBusy()

    def set_position_ok(self, position):
        self.positions[position].SendResponse()
        self.message += '{}: OK!\n'.format(position)

    def setP_position_ready(self, position):
        self.positions[position].ChangeStateToReady()
        self.message += '{}: Ready!\n'.format(position)

    #=========#
    # Methods #
    #=========#
    def build_position_list(self):
        self.positions = [None]
        self.machines = [None] + [0] * self.num_pos
        for i in range(1, len(self.num_pos)+1):
            self.positions.append(Position(i, 0, self.get_player_list_of_position(i)))
            self.machines.append(0)
        preset_positions = self.config.options('Preset')
        for pos in preset_positions:
            self.set_machine_to_position(self.config.getint('Preset', pos), int(pos))
        self.set_machine_auto()

    def load_rule_wave(self):
        ruleconfig = configuration.SectionConfig('rules/'+self.rulename, self.get_stage())
        self.rule_wave = int(ruleconfig['wave'])

    def send_check(self, machine):
        if self.check:
            self.check(machine)

    def save_wave(self, message):
        db_msg = {
            'action' = 'savewave',
            'tag' = message['player'],
            'shots' = message['score'],
            'wave' = self.get_wave()
            'stage' = self.get_stage().self.get_substage()
        }
        resp = DBAccess.request(db_msg)

        pos = self.getPositionByPlayerTag(message['player'])
        self.positions[pos].SetPlayerFlag(message['player'])
        if self.positions[pos].AllBack():
            self.send_check(int(self.getMachineByPosition(pos)))
            self.positions[pos].ResetFlags()
        self.message += message['message'] + '\n'

    def clear(self):
        self.wave = 1
        self.positions = self.build_position_list()

    def next_wave(self):
        self.wave += 1

    def position_is_busy(self, position):
        return self.positions[position].IsBusy()

    def save_config(self):
        with open('status.cfg', 'w') as configfile
            self.config.write(configfile)

    def unlink(self, position):
        self.position[position].machine = 0
        self.machines[position] = 0
