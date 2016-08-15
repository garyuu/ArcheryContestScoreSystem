'''
Author: Garyuu
Date:   2016/8/15
Name:   status
Descr.: Save all core status and settings.
'''
from sql_wrapper import SQLWrapper
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
    wrapper = SQLWrapper(
        self.sql_config['host'],
        self.sql_config['user'],
        self.sql_config['password'],
        self.sql_config['database']
    )

    def __init__(self):
        self.mode = ModeEnum(int(self.config.get('Contest', 'mode')))
        self.wave = int(self.config.get('Contest', 'wave'))
        self.rulename = self.config.get('Contest', 'rulename')
        self.num_pos = int(self.config.get('Position', 'number'))
        self.positions = self.buildPositionList(self.config.get('Position', 'positionlist'))
        slef.rule = configuration.Config('rules/'+self.rulename)

    def buildPositionList(self, string):
        ary = string.split(',')
        pos = [None]
        for i in ary:
            pos.append(Position(i))
        return pos

    def getMacineList(self):
        machines = []
        for pos in self.positions:
            machines.append(pos.id) if pos != None else machines.append(None)
        return machines

    def getMachineByPosition(self, position):
        return self.positions[position].id

    def getPlayersListOfPosition(self, position):
        return self.wrapper.GetPlayerListByPosition(position)

    def getNumberOfPlayersOfPosition(self, position):
        return len(self.getPlayersListOfPosition(position))

    def getScore(self, player_position):
        scores = self.wrapper.GetScoreByPlayerPosition(player_position)
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

    def setMachineToPosition(self, machine, position):
        self.positions[position].id = machine

    def loadRule(self, rulename):
        self.rulename = rulename
        self.rule.read('rules/'+self.rulename)

    def saveWave(self, message):
        self.wrapper.AddWave(
            self.mode.value,
            int(message['wave']),
            self.wrapper.,
            self.config.get('Contest', 'stage') + self.config.get('Contest', 'substage')),
            message['score']
        )
            

    def display_all(self):

    def __str__(self):

    
