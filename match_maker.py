'''
Author: Garyuu
Date:   2016/8/30
Name:   match_maker
Descr.: Deal with match making. Also the controller of substage.
        Save section infomation.
'''
import dbaccess
import random
import match_table

class MatchMaker:
    def make(player_list, group, q_to_d=False, split=0):
        if q_to_d:
            plist = MatchMaker.prepare_list(player_list)
        else:
            plist = player_list
        return MatchMaker.make_promote(plist, group, split, q_to_d)

    def prepare_list(player_list):
        player_list.sort(key=MatchMaker.cmp_to_key(MatchMaker.cmp))
        player_list.reverse()
        promote_num = len(player_list) #get total # of players
        while promote_num & (-promote_num) != promote_num: #if promote is not 2**k, turn into 2**k
            promote_num -= promote_num & (-promote_num)
        plist = player_list[:promote_num]
        for i in range(promote_num):
            plist[i].rank = i + 1
        return plist

    def make_promote(player_list, group, split, first_round):
        player_num = len(player_list)
        if not first_round and split:
            round_size = player_num
        else:
            round_size = player_num // 2
        result = []
        table = match_table.position_rank_table[group][round_size]
        if first_round:
            for p in player_list:
                new_pos = table[p.rank-1]
                quart_size = round_size // 4
                if split and p.rank > quart_size and p.rank <= quart_size * 3:
                    result.append((p.tag, new_pos, p.rank, True))
                else:
                    result.append((p.tag, new_pos, p.rank))
        else:
            for p in player_list:
                if p.winner:
                    rank = p.rank if p.rank <= round_size else (round_size * 2 + 1 - p.rank)
                    new_pos = table[rank-1]
                    result.append((p.tag, new_pos, rank))
        return result

    def send_stage_positions(result, stage, team, splitmode=False):
        db_msg = {
            'action': 'savestageposition',
            'table': [],
            'team': team,
        }
        sub = len(result) if not splitmode else (len(result) * 2)
        for row in result:
            data = {
                'stage': stage + str(sub),
                'tag': row[0],
                'position': row[1],
                'rank': row[2]
            }
            if len(row) > 3:
                data['filter'] = stage + str(sub*2)
            else:
                data['filter'] = None
            db_msg['table'].append(data)
        dbaccess.DBAccess.request(db_msg)

    def cmp(a,b):
        if a.total_score() != b.total_score():
            return a.total_score() - b.total_score()
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
            elif a.winner != b.winner:
                return a.winner - b.winner
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
'''
