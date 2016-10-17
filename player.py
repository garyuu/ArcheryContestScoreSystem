'''
Author: Garyuu
Date:   2016/10/16
Name:   player
Descr.: To store a player's data.
'''
from dbaccess import DBAccess
class Player:
    def __init__(self, id, tag, position, stage, group):
        self.id = id
        self.tag = tag
        self.position = position
        self.stage = stage
        self.group = group
        self.wave_list = []
        self.score_list = []
        self.winner = False

    def add_wave(self, shot1=-1, shot2=-1, shot3=-1, shot4=-1, shot5=-1, shot6=-1):
        self.wave_list.append([shot1, shot2, shot3, shot4, shot5, shot6])

    def add_wave_from_list(self, shots):
        self.add_wave(shot[0], shot[1], shot[2], shot[3], shot[4], shot[5])

    def add_score(self, score):
        self.score_list.append(score)

    def latest_wave_sum(self):
        total = 0
        for i in self.wave_list[-1]:
            if i == 11:
                total += 10
            elif i > 0 and i <= 10:
                total += i
        self.score_list.append(total)

    def latest_wave_save(self):
        db_msg = {
            'action'    : 'savewave',
            'wave'      : self.wave_count,
            'tag'       : self.tag,
            'stage'     : self.stage,
            'position'  : self.position,
            'score'     : self.score_list[-1],
            'shots'     : self.wave_list[-1],
            'winner'    : self.winner,
        }
        DBAccess.request(db_msg)

    def wave_count(self):
        return len(self.wave_list)

    def total_score(self):
        total = 0
        for i in score_list:
            total += i
        return total
