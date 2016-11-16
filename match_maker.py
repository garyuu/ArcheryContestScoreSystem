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
            result = self.group_make_qtod(player_list, bound)
        else:
            result = self.group_make_dtod(player_list, bound)
        return result

    def make_qtod(self, player_list, bound):
        player_list.sort(key=MatchMaker.cmp_to_key(MatchMaker.cmp))

        promote_num = len(player_list) #get total # of players

        while promote_num & (-promote_num) != promote_num: #if promote is not 2**k, turn into 2**k
            promote_num -= promote_num & (-promote_num)

        pos_num = bound[1] - bound[0] + 1 #get total # of position

        while pos_num & (-pos_num) != pos_num: #if pos is not 2**k, turn into 2**k
            pos_num -= pos_num & (-pos_num)
        
        i = 0
        result = []
        while i * 2 <= promote_num:
            player_sublist = player_list[i:i+pos_num*2]

            for idx in range(0,pos_num//2):
                player_sublist[idx*2].position = pos_num//2 + (bound[0] - 1) - idx
                player_sublist[-idx*2-1].position = pos_num//2 + (bound[0] - 1) - idx
                # 1 vs 16 at 4
                player_sublist[idx*2 + 1].position = pos_num//2 + (bound[0] - 1) + idx + 1
                player_sublist[-idx*2 - 2].position = pos_num//2 + (bound[0] - 1) + idx + 1
                # 2 vs 15 at 5
            
            for idx in range(0,pos_num*2):
                if i > 0:
                    result.append((player_sublist[idx].tag,player_sublist[idx].position, True))
                else:
                    result.append((player_sublist[idx].tag,player_sublist[idx].position))

            i += pos_num*2

        return result

    def make_dtod(self, player_list, bound):
        player_num = len(player_list)
        current_rank_of_position = self.position_of_rank_generator(player_num, bound, True)
        new_position_of_rank = self.position_of_rank_generator(player_num/2, bound)
        result = []
        for p in player_list:
            if p.winner:
                new_pos = new_position_of_rank[current_rank_of_position[p.position]]
                result.append((p.tag, new_pos))
        return result

    def send_stage_positions(self, result, stage, team):
        db_msg = {
            'action' = 'savestageposition',
            'table' = [],
            'team' = team,
        }
        for row in result:
            data = {
                'stage': stage + str(len(result)),
                'tag': row[0],
                'position': row[1],
            }
            if len(row) > 2:
                data['filter'] = stage +  str(row[2]))
            else:
                data['filter'] = None
            db_msg['table'].append(data)
        DBAccess.request(db_msg)

    def position_of_rank_generator(size, bound, reverse=False, rec=False):
        if rec:
            if size == 1:
                return [[1,2]]
            else
                table = self.position_of_rank_generator(size/2, None, False, True)
                result = []
                for x in table:
                    for y in x:
                        result.append([y, size*2+1-y])
                return result
        else:
            one_by_one = 4  # Set below(include) how many size assign one position for one player
            table = self.position_of_rank_generator(size, None, False, True)
            pos_num = bound[1] - bound[0] + 1
            while pos_num & (-pos_num) != pos_num:
                pos_num -= pos_num & (-pos_num)
            result = {}
            if size > one_by_one:
                if size == 1:
                    start = (pos_num - 2) / 2 + bound[0]
                    table.append([3,4])
                else:
                    start = (pos_num - size) / 2 + bound[0]
                for x in range(0, len(table)):
                    for y in table[x]:
                        result[y] = x + start
            else:
                if size == 1:
                    start = (pos_num - 4) / 2 + bound[0]
                    table.append([3,4])
                else:
                    start = (pos_num - size * 2) / 2 + bound[0]
                i = start
                for x in table:
                    for y in x:
                        result[y] = i
                        i += 1
            if reverse:
                origin_result = result
                result = {}
                for rank in origin_result:
                    if rank <= size:
                        result[origin_result[rank]] = rank
            return result

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
