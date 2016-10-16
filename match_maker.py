'''
Author: Garyuu
Date:   2016/8/30
Name:   match_maker
Descr.: Deal with match making. Also the controller of substage.
        Save section infomation.
'''
import enum
import dbaccess

class MatchMaker:
    def make(self, player_list, q_to_d=False):
        if q_to_d:
            self.group_make_qtod(player_list)
        else:
            self.group_make_dtod(player_list)

    def make_qtod(self, group):
        # TODO MM from qualifying to dual match


        pass

    def make_dtod(self, group):
        # TODO MM to eliminate players from dual match
        pass

    def cmp(a,b):
        if a.total != b.total:
            return a.total<b.total
        else:
