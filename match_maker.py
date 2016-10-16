'''
Author: Garyuu
Date:   2016/8/30
Name:   match_maker
Descr.: Deal with match making. Also the controller of substage.
        Save section infomation.
'''
import enum
import dbaccess
import random

class MatchMaker:
    def make(self, player_list, q_to_d=False):
        if q_to_d:
            self.group_make_qtod(player_list)
        else:
            self.group_make_dtod(player_list)

    def make_qtod(self, group):
        # TODO MM from qualifying to dual match
        player_list.sort(cmp)

        pass

    def make_dtod(self, group):
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
                return (a_ten + a_elev) - (b_ten + b_elev):
            elif a_elev != b_elev:
                return a_elev - b_elev:
            else:
                return random.choice((1,-1))
