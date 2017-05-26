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
        if simplify == True:
            output = "Tag = {} Position = {} Score = {}\n".format(self.tag, self.position, self.score_list)
        else:
            blank = "   "*(7-len(self.wave_list[0]))
            output = "Group = {}\nTag = {} Position = {}\n\n".format(self.group, self.tag, self.position)
            output += " "*21 + "Score   Point\n"
            for i in range(len(self.wave_list)):
                for j in range(len(self.wave_list[i])):
                    output += "{:>3}".format(self.wave_list[i][j])
                output += blank
                output += "{:>5}   {:>5}\n".format(self.score_list[i], self.point_list[i])
            output += " "*17 + "Total Score = {:>3}\n".format(self.total_score())
        return output
        
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
                score += int(shot)
        self.score_list[index] = score
        

    def total_score(self):
        sum_score = 0
        for score in self.score_list:
            if score is not None:
                sum_score += score
        return sum_score

if __name__=="__main__" :
    player = Player(45, "AB", 98, 2, "c")
    player.add_wave(1,["X", "10", "9", "7", "5", "m"])
   # player.add_wave(2,["X", "X", "8", "7", "5", "4"])
   # player.add_wave(3,["10", "10", "5", "3", "m", "m"])
    player.point_list = [2, 2, 2]
    
    print(player)