'''
Author: NekOrz, Garyuu
Date:   2016/8/15
Name:   position
Descr.: The object that serves as a signal/timer thingy
'''
class Position():
    def __init__(self, position, player_list):
        self.id = position
        self.machine = None
        self.player_list = player_list

    def __str__(self, simplify = False):
        #TODO Display message
        pass

    def assign_machine(self, machine):
        if self.machine == None or self.machine == machine:
            self.machine = machine
            return True
        else:
            return False

    def wave_count(self):
        count = []
        for player in player_list:
            count.append(len(player.wave_list))
        return max(count)
