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

    def __init__(self, check):
        """
        self.wrapper = SQLWrapper(
            self.sql_config['host'],
            self.sql_config['user'],
            self.sql_config['password'],
            self.sql_config['database']
        )
        """
        self.check = check
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
            pos.append(Position(int(i), self.getPlayersListOfPosition(i)))
        return pos

    def getMacineList(self):
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

    def setMachineToPosition(self, machine, position):
        self.positions[position].id = machine

    def loadRule(self, rulename):
        self.rulename = rulename
        self.rule.read('rules/'+self.rulename)

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
            self.check(self.getMachineByPosition(pos))
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

    def __str__(self):
        msg = 'Mode: {}, Wave {}\n'.format(self.mode.name, self.wave)
        msg += 'Stage: {}-{}\n'.format(self.stage, self.substage)
        for i in range(0, len(self.positions)):
            msg += '{}: {}\n'.format(i, self.positions[i])
        msg += 'Messages:\n' + self.message
        return msg
