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
    def __init__(self, pid, mid, player_list):
        self.id = pid
        self.machine = mid
        self.players = player_list
        self.state = StateEnum.unknown
        self.waiting = False
        self.dead = False
        self.flags = dict()
    
    def __str__(self):
        string = "{}: ".format(self.id)
        string += "[X]" if self.dead else "[ ]"
        string += "M{}. ".format(self.machine)
        string += "State: {}".format(self.state.name)
        string += ", waiting..." if self.waiting else ""
        if self.state == StateEnum.busy:
            if self.all_back():
                string += ", All sent back"
            else:
                string += ", Sent back:"
                for player in self.flags:
                    string += " {},".format(player)
                string += " Still {}".format(len(self.players)-len(self.flags))
        return string

    def change_state_to_ready(self):
        self.state = StateEnum.ready

    def change_state_to_busy(self):
        self.state = StateEnum.busy
    
    def wait_for_response(self,sec = 10.0):
        self.waiting = True
        self.timer = threading.Timer(sec,self.SetDead)
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

    def is_busy(self):
        return self.state == StateEnum.busy
        
def main():
    pass
    
if __name__ == '__main__':
    main()
