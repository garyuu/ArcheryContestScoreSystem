'''
Author: Garyuu
Date:   2016/10/16
Name:   player
Descr.: To store a player's data.
'''
class Player:
    def __init__(self, id, tag, position, rank, group):
        self.id = id
        self.tag = tag
        self.position = position
        self.rank = rank
        self.wave_list = []
        self.score_list = []
        self.point_list = []
        self.winner = False
        self.group = group

    def __str__(self, simplify = False):
        #TODO Display message
        pass

    def add_wave(self, count, shots):
        if len(self.wave_list) < count:
            to_extend = [None] * (count - len(self.wave_list))
            self.wave_list.extend(to_extend)
            self.score_list.extend(to_extend)
            self.point_list.extend(to_extend)
        if not self.wave_list[count-1]:
            self.wave_list[count-1] = shots
            self.raw_score_calculate(count)
    
    def raw_score_calculate(self, count):
        index = count - 1
        score = 0
        for shot in self.wave_list[index]:
            if shot == 'X':
                score += 10
            elif shot == 'm':
                pass
            else:
                score += int(i)
        self.score_list[index] = score

    def total_score():
        sum_score = 0
        for score in self.score_list:
            if score is not None:
                sum_score += score

