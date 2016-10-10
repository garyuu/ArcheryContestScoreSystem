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
    Empty = -1
    Idle = 0
    Ready = 1
    Sleeping = 2
    Received = 3
    Receiving = 4

class Position():
    def __init__(self, pid, mid, player_list):
        self.id = pid
        self.machine = mid
        self.players = player_list
        self.state = StateEnum.Empty
        self.waiting = False
        self.dead = False
        self.flags = dict()
    
    def __str__(self):
        string = "{}: ".format(self.id)
        string += "[X]" if self.dead else "[ ]"
        string += "M{}. ".format(self.machine)
        string += "State: {}".format(self.state.name)
        string += ", waiting..." if self.waiting else ""
        if self.state == StateEnum.Receiving:
            string += ", Sent back:"
            for player in self.flags:
                string += " {},".format(player)
            string += " Still {}".format(len(self.players)-len(self.flags))
        return string

    def change_state(self, state):
        self.state = StateEnum[state]

    def wait_for_response(self,sec = 10.0):
        self.waiting = True
        self.timer = threading.Timer(sec,self.set_dead)
        self.timer.start()
        
    def set_dead(self):
        self.dead = True
    
    def received_response(self):
        self.timer.cancel()
        self.waiting = False
        self.dead = False
    
    def set_player_flag(self, player):
        if player in self.players:
            self.flags[player] = True

    def reset_flags(self):
        self.flags = dict()

    def all_back(self):
        return len(self.flags) == len(self.players)

    def is_ready(self):
        return self.state == StateEnum.Ready
        
def main():
    pass
    
if __name__ == '__main__':
    main()
