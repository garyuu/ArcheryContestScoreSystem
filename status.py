'''
Author: Garyuu
Date:   2016/8/15
Name:   status
Descr.: Save all core status and settings.
'''
import sql_wrapper as sql
import configuration
from position import Position
from enum import Enum

class ModeEnum(Enum):
    qualiying = 1
    dual = 2
    team = 3

class Status():
    config = configuration.Config('status')

    def __init__():
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

    def getMacineList():
        machines = []
        for pos in self.positions:
            machines.append(pos.id) if pos != None else machines.append(None)
        return machines

    def getMachineByPosition(position):
        return self.positions[position].id

    def setWait(position):
        self.positions[position].wait()

    def setMachineToPosition(machine, position):
        self.positions[position].machine = machine

    def loadRule(rulename):
        self.rulename = rulename
        self.rule.read('rules/'+self.rulename)

    def saveWave(message):


    def display_all():

    def __str__():

    
