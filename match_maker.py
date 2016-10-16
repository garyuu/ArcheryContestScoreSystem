'''
Author: Garyuu
Date:   2016/8/30
Name:   match_maker
Descr.: Deal with match making. Also the controller of substage.
        Save section infomation.
'''
#from player import Player
import enum
import dbaccess
import random

class MatchMaker:
    def make(self, player_list, bound, q_to_d=False):
        if q_to_d:
            self.group_make_qtod(player_list, bound)
        else:
            self.group_make_dtod(player_list, bound)

    def make_qtod(self, player_list, bound):
        player_list.sort(key=MatchMaker.cmp_to_key(MatchMaker.cmp))

        pos_num = bound[1] - bound[0] + 1 #get total # of position

        while pos_num & (-pos_num) != pos_num: #if pos is not 2**k, turn into 2**k
            pos_num -= pos_num & (-pos_num)

        player_list = player_list[0:pos_num*2]

        for idx in range(0,pos_num//2):
            player_list[idx*2].position = pos_num//2 + (bound[0] - 1) - idx
            player_list[-idx*2-1].position = pos_num//2 + (bound[0] - 1) - idx
            # 1 vs 16 at 4
            player_list[idx*2 + 1].position = pos_num//2 + (bound[0] - 1) + idx + 1
            player_list[-idx*2 - 2].position = pos_num//2 + (bound[0] - 1) + idx + 1
            # 2 vs 15 at 5
            
        result = []
        for idx in range(0,pos_num*2):
            result.append((player_list[idx].tag,player_list[idx].position))
        return result

    def make_dtod(self, player_list, bound):
        # TODO MM to eliminate players from dual match
        pass

    def cmp(a,b):
        if a.total != b.total:
            return a.total - b.total
        else:
            a_ten = 0
            a_elev = 0
            b_ten = 0
            b_elev = 0
            for wave in a.wave_list:
                for score in wave:
                    if score == 10:
                        a_ten += 1
                    elif score == 11:
                        a_elev += 1

            for wave in b.wave_list:
                for score in wave:
                    if score == 10:
                        b_ten += 1
                    elif score == 11:
                        b_elev += 1

            if (a_ten + a_elev) != (b_ten + b_elev):
                return (a_ten + a_elev) - (b_ten + b_elev)
            elif a_elev != b_elev:
                return a_elev - b_elev
            else:
                return random.choice((1,-1))

    def cmp_to_key(mycmp):
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K
'''
if __name__ == "__main__":
    l = []
    for i in range(1,23):
        a = Player(i,i,i,i,i)
        a.add_wave(61,[10,10,10,10,11,10])
        l.append(a)
    f = MatchMaker().make_qtod(l,(1,8))

    print(f)
'''
