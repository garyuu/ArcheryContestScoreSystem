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
    def make(self, player_data, q_to_d=False):
        for group in player_data.groups:
            if q_to_d:
                self.group_make_qtod(group)
            else:
                self.group_make_dtod(group)

    def group_make_qtod(self, group):
        # TODO MM from qualifying to dual match
        pass

    def group_make_dtod(self, group):
        # TODO MM to eliminate players from dual match
        pass
