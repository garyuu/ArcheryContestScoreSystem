'''
Author: NekOrz, Garyuu
Date:   2016/8/15
Name:   position
Descr.: The object that serves as a signal/timer thingy
'''
#import time
import threading
from enum import Enum

class StateEnum(Enum):
    unknown = 0
    ready = 1
    busy = 2
    

class Position():
    def __init__(self,id,players):
        self.id = id
        self.state = StateEnum.unknown
        self.waiting = False
        self.dead = False
        self.players = players
        self.flags = dict()
    
    def __str__(self):
        string = "[X]" if self.dead else "[ ]"
        string += "M{}. ".format(self.id)
        string += "State: {}".format(self.state.name)
        string += ", waiting..." if self.waiting else ""
        if self.state == StateEnum.busy:
            if self.AllBack():
                string += ", All sent back"
            else:
                string += ", Sent back:"
                for player in self.flags:
                    string += " {},".format(player)
                string += " Still {}".format(len(self.players)-len(self.flags))
        return string

    def ChangeStateToReady(self):
        self.state = StateEnum.ready

    def ChangeStateToBusy(self):
        self.state = StateEnum.busy
    
    def WaitForResponse(self,sec = 10.0):
        self.waiting = True
        self.timer = threading.Timer(sec,self.SetDead)
        self.timer.start()
        
    def SetDead(self):
        self.dead = True
    
    def SendResponse(self):
        self.timer.cancel()
        self.waiting = False
        self.dead = False
    
    def SetPlayerFlag(self, player):
        if player in self.players:
            self.flags[player] = True

    def ResetFlags(self):
        self.flags = dict()

    def AllBack(self):
        return len(self.flags) == len(self.players)

    def IsBusy(self):
        return self.state == StateEnum.busy
        
def main():
    p = Position(1, ['1A', '1B', '1C'])
    
    p.WaitForResponse(1)
    print("YAY!")
    print(p)
    #while p.waiting:
    #    print(p)
    p.SendResponse()
    print(p)
    p.ChangeStateToBusy()
    print(p)
    p.SetPlayerFlag('1B')
    p.SetPlayerFlag('1C')
    print(p)
    p.SetPlayerFlag('1A')
    print(p)
    p.ResetFlags()
    print(p)
    
if __name__ == '__main__':
    main()
