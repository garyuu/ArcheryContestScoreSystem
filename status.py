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
    qualiying = 1
    dual = 2
    team = 3

class Status:
    config = configuration.Config('status')
    sql_config = configuration.SectionConfig('sql', 'SQL')
    '''wrapper = SQLWrapper(
        self.sql_config['host'],
        self.sql_config['user'],
        self.sql_config['password'],
        self.sql_config['database']
    )'''

    def __init__(self):
        self.mode = ModeEnum(int(self.config.get('Contest', 'mode')))
        self.wave = int(self.config.get('Contest', 'wave'))
        self.rulename = self.config.get('Contest', 'rulename')
        self.num_pos = int(self.config.get('Position', 'number'))
        self.positions = self.buildPositionList()
        self.rule = configuration.Config('rules/'+self.rulename)
        self.message = ''
        self.stage = self.config.get('Contest', 'stage')
        self.substage = self.config.get('Contest', 'substage')

    def buildPositionList(self):
        ary = self.config.get('Position', 'positionlist').split(',')
        pos = [None]
        for i in ary:
            pos.append(Position(self.getNumberOfPlayersOfPosition(i), int(i)))
        return pos

    def getMacineList(self):
        machines = []
        for pos in self.positions:
            machines.append(pos.id) if pos != None else machines.append(None)
        return machines

    def getMachineByPosition(self, position):
        return self.positions[position].id

    def getPlayersListOfPosition(self, position):
        #return self.wrapper.GetPlayerListByPosition(position)
        return ['1A', '1B', '1C', '1D']

    def getNumberOfPlayersOfPosition(self, position):
        #return len(self.getPlayersListOfPosition(position))
        return 4

    def getScore(self, player_position):
        #scores = self.wrapper.GetScoreByPlayerPosition(player_position)
        scores = [['X', '9', '7', '5', '1', 'm']]
        total = 0
        for wave in scores:
            for i in wave:
                if i == 11:
                    total += 10
                elif i >= 0:
                    total += i
        return total

    def setWait(self, position):
        self.positions[position].ChangeStateToWait()
        self.message += 'Wait for position {} to respond.\n'.format(position)

    def setMachineToPosition(self, machine, position):
        self.positions[position].id = machine

    def loadRule(self, rulename):
        self.rulename = rulename
        self.rule.read('rules/'+self.rulename)

    def saveWave(self, message):
        '''
        self.wrapper.AddWave(
            self.mode.value,
            int(message['wave']),
            self.wrapper.GetIdByPos(message['player']),
            self.stage + self.substage,
            message['score']
        )
        '''
        self.positions[int(message['player'][:-1])].AddCount()
        self.message += message['message'] + '\n'

    def setPositionOk(self, position):
        self.positions[position].state = 1
        self.message += '{}: OK!\n'.format(position)

    def clear(self):
        self.wave = 1
        self.positions = buildPositionList()

    def __str__(self):
        msg = 'Mode: {}, Wave {}'.format(self.mode.name, self.wave)
        msg = 'Stage: {}-{}\n'.format(self.stage, self.substage)
        for i in range(0, len(self.positions)):
            msg += '{}: {}\n'.format(i, self.positions[i])
        msg += 'Messages:\n' + self.message
        return msg
