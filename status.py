'''
Author: Garyuu
Date:   2016/8/15
Name:   status
Descr.: Save all core status and settings.
'''
#from sql_wrapper import SQLWrapper
import configuration
from position import Position
from enum import Enum

class ModeEnum(Enum):
    Qualiying       = '1'
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
        self.build_position_list()

    def __del__(self):
        self.save_config()

    def __str__(self):

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

    #=====#
    # Set #
    #=====#
    def set_mode(self, mode): # mode should be str
        self.config.set('Contest', 'mode', ModeEnum[mode].value)
        self.config.set('Contest', 'stage', mode)
        self.load_rule_wave()

    def set_wave(self, wave): # wave should be int
        self.config.set('Contest', 'wave', str(wave))

    def set_rulename(self, rulename):
        self.config.set('Contest', 'rulename', rulename)
        self.load_rule(rulename)

    def set_substage(self, substage):
        self.config.set('Contest', 'wave', substage)

    def set_machine_to_position(self, machine, position, nosave=False):
        if machine in self.machines:

        self.positions[position].id = machine

    #=========#
    # Methods #
    #=========#
    def build_position_list(self):
        self.positions = [None]
        self.machines = [None]
        for i in range(1, len(self.num_pos)+1):
            self.positions.append(Position(i, i, self.get_player_list_of_position(i)))
            self.machines.append(i)
        preset_positions = self.config.options('Preset')
        for pos in preset_positions:
            self.set_machine_to_position()

    def get_machine_list(self):
        machines = []
        for pos in self.positions:
            machines.append(pos.id) if pos != None else machines.append(None)
        return machines

    def getMachineByPosition(self, position):
        return self.positions[position].id

    def getPlayersListOfPosition(self, position):
        #return self.wrapper.GetPlayerTagByPos(position)
        return ['1A', '1B', '1C', '1D']

    def getNumberOfPlayersOfPosition(self, position):
        return len(self.getPlayersListOfPosition(position))

    def getScore(self, player_position):
        """
        scores = self.wrapper.GetScoreByPlayerPosition(player_position)
        total = 0
        for wave in scores:
            for i in wave:
                j = int(i)
                if j == 11:
                    total += 10
                elif j >= 0:
                    total += j
        return total
        """
        return 168

    def getPositionByPlayerTag(self, tag):
        for i in range(1, len(self.positions)):
            if tag in self.positions[i].players:
                return i

    def setWait(self, position):
        self.positions[position].WaitForResponse()
        self.message += 'Wait for position {} to respond.\n'.format(position)


    def load_rule_wave(self):
        ruleconfig = configuration.SectionConfig('rules/'+self.rulename, self.get_stage())
        self.rule_wave = int(ruleconfig['wave'])

    def sendCheck(self, machine):
        if self.check:
            self.check(machine)

    def saveWave(self, message):
        """
        self.wrapper.AddWave(
            self.mode.value,
            int(message['wave']),
            self.wrapper.GetIdByTag(message['player']),
            self.stage + self.substage,
            message['score']
        )
        """
        pos = self.getPositionByPlayerTag(message['player'])
        self.positions[pos].SetPlayerFlag(message['player'])
        if self.positions[pos].AllBack():
            self.sendCheck(int(self.getMachineByPosition(pos)))
            self.positions[pos].ResetFlags()
        self.message += message['message'] + '\n'
    
    def setPositionBusy(self, position):
        self.positions[position].ChangeStateToBusy()

    def setPositionOk(self, position):
        self.positions[position].SendResponse()
        self.message += '{}: OK!\n'.format(position)

    def setPositionReady(self, position):
        self.positions[position].ChangeStateToReady()
        self.message += '{}: Ready!\n'.format(position)

    def clear(self):
        self.wave = 1
        self.positions = self.buildPositionList()

    def nextWave(self):
        self.wave += 1

    def positionIsBusy(self, position):
        return self.positions[position].IsBusy()

    def save_config(self):
        with open('status.cfg', 'w') as configfile
            self.config.write(configfile)

