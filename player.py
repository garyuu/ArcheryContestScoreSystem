'''
Author: Garyuu
Date:   2016/10/16
Name:   player
Descr.: To store a player's data.
'''
class Player:
    def __init__(self, id, position, stage, group):
        self.id = id
        self.position = position
        self.stage = stage
        self.group = group
        self.total = 0
        self.wave_list = []
    
    def add_wave(self, score, shot1=-1, shot2=-1, shot3=-1, shot4=-1, shot5=-1, shot6=-1):
        self.total += score
        self.wave_list.append([shot1, shot2, shot3, shot4, shot5, shot6])

    def wave_count(self):
        return len(self.wave_list)
