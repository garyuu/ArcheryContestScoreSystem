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

    def __str__(self):
        output = "{}- Group: {} Winner: {} Total score: {}".format(
            self.tag, self.group, self.winner, self.total_score()) + "\n"
        for i in range(len(self.wave_list)):
            output += "    [{}] : {}".format(i, str(self.wave_list[i]) + ", " + str(self.score_list[i])) + "\n"
        return output

    def add_wave(self, shot1=-1, shot2=-1, shot3=-1, shot4=-1, shot5=-1, shot6=-1):
        self.wave_list.append([shot1, shot2, shot3, shot4, shot5, shot6])

    def add_wave_from_list(self, shots):
        self.add_wave(shots[0], shots[1], shots[2], shots[3], shots[4], shots[5])

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
            'wave'      : self.wave_count(),
            'tag'       : self.tag,
            'stage'     : self.stage,
            'score'     : self.score_list[-1],
            'shots'     : self.wave_list[-1],
            'winner'    : self.winner,
        }
        DBAccess.request(db_msg)

    def wave_count(self):
        return len(self.wave_list)

    def total_score(self):
        total = 0
        for i in self.score_list:
            total += i
        return total

    def send_winner_change(self):
        db_msg = {
            'action': 'modifywinner',
            'stage': self.stage,
            'wave': self.wave_count(),
            'tag': self.tag,
            'win': self.winner,
        }
        DBAccess.request(db_msg)

'''
def main():
    p = Player(1, 1A, )
    pass

if __name__ == '__main__':
    main()
'''
