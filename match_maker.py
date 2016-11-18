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
    def make(player_list, bound, q_to_d=False, split=0):
        if q_to_d:
            result = MatchMaker.make_qtod(player_list, bound)
        else:
            result = MatchMaker.make_dtod(player_list, bound, split)
        return result

    def promote_calculate(plist, table, filtermode=False):
        result = []
        for idx in range(half_pos):
            if filtermode:
                result.append((plist[idx].tag, plist[idx].position, len(plist)*4))
            else:
                result.append((plist[idx].tag, plist[idx].position))
        return result

    def make_qtod(player_list, bound):
        player_list.sort(key=MatchMaker.cmp_to_key(MatchMaker.cmp))

        promote_num = len(player_list) #get total # of players

        while promote_num & (-promote_num) != promote_num: #if promote is not 2**k, turn into 2**k
            promote_num -= promote_num & (-promote_num)

        pos_num = bound[1] - bound[0] + 1 #get total # of position

        while pos_num & (-pos_num) != pos_num: #if pos is not 2**k, turn into 2**k
            pos_num -= pos_num & (-pos_num)
        
        result = []
        new_position_of_rank = MatchMaker.position_of_rank_generator(promote_num//2, bound)
        if promote_num <= pos_num:
            for idx in range(promote_num):
                result.append(player_list[idx].tag, new_position_of_rank[idx+1])
        else:
            quart_promote = promote_num // 4
            for idx in range(promote_num):
                if idx < quart_promote or idx >= quart_promote * 3:
                    result.append(player_list[idx].tag, new_position_of_rank[idx+1], True)
                else:
                    result.append(player_list[idx].tag, new_position_of_rank[idx+1])
        return result

    def make_dtod(player_list, bound, split=0):
        player_num = len(player_list)
        size = player_num if split == 0 else player_num * 2
        current_rank_of_position = MatchMaker.position_of_rank_generator(size, bound, True, split)
        new_position_of_rank = MatchMaker.position_of_rank_generator(size//2, bound, False, split)
        result = []
        for p in player_list:
            if p.winner:
                new_pos = new_position_of_rank[current_rank_of_position[p.position]]
                result.append((p.tag, new_pos))
        return result

    def send_stage_positions(result, stage, team, splitmode):
        db_msg = {
            'action': 'savestageposition',
            'table': [],
            'team': team,
        }
        sub = str(len(result)) if not splitmaode else str(len(result)*2)
        for row in result:
            data = {
                'stage': stage + str(len(result)),
                'tag': row[0],
                'position': row[1],
            }
            if len(row) > 2:
                data['filter'] = stage + sub
            else:
                data['filter'] = None
            db_msg['table'].append(data)
        dbaccess.DBAccess.request(db_msg)

    def position_of_rank_generator(size, bound, reverse=False, split=0, rec=False):
        if rec:
            if size <= 1:
                return [[1,2]]
            else:
                table = MatchMaker.position_of_rank_generator(size//2, None, False, 0, True)
                result = []
                for x in table:
                    for y in x:
                        if len(table) == 1:
                            if x.index(y):
                                result.append([y, size*2+1-y])
                            else:
                                result.append([size*2+1-y, y])
                        else:
                            if table.index(x) >= len(table) // 2:
                                result.append([y, size*2+1-y])
                            else:
                                result.append([size*2+1-y, y])
                return result
        else:
            one_by_one = 2  # Set below(include) how many size assign one position for one player
            table = MatchMaker.position_of_rank_generator(size, None, False, 0, True)
            bound_width = bound[1] - bound[0] + 1
            pos_num = bound_width 
            while pos_num & (-pos_num) != pos_num:
                pos_num -= pos_num & (-pos_num)
            one_by_one = one_by_one if one_by_one <= pos_num // 2 else pos_num // 2
            result = {}
            if size > one_by_one:
                if size == 1:
                    table.append([3,4])
                if pos_num >= len(table):
                    start = (bound_width - len(table)) // 2 + bound[0]
                    for x in range(len(table)):
                        for y in table[x]:
                            result[y] = x + start
                else:
                    start = (bound_width - len(table) // 2) // 2 + bound[0]
                    quart_table = len(table) // 4
                    if quart_table:
                        table_outer = table[:quart_table] + table[quart_table*3:]
                        table_inner = table[quart_table:quart_table*3]
                    else:
                        table_outer = table[1] if size == 1 else table[0]
                        table_inner = table[0] if size == 1 else table[1]
                    for x in range(len(table_outer)):
                        for y in table_outer[x]:
                            result[y] = x + start
                    for x in range(len(table_inner)):
                        for y in table_inner[x]:
                            result[y] = x + start
            else:
                if size == 1:
                    table.append([3,4])
                if pos_num >= len(table) * 2:
                    start = (bound_width - len(table) * 2) // 2 + bound[0]
                    i = start
                    for x in table:
                        for y in x:
                            result[y] = i
                            i += 1
                else:
                    start = (bound_width - len(table)) // 2 + bound[0]
                    quart_table = len(table) // 4
                    if quart_table:
                        table_outer = table[:quart_table] + table[quart_table*3:]
                        table_inner = table[quart_table:quart_table*3]
                    else:
                        table_outer = table[1] if size == 1 else table[0]
                        table_inner = table[0] if size == 1 else table[1]
                    i = start
                    for x in table_outer:
                        for y in x:
                            result[y] = i
                            i += 1
                    i = start
                    for x in table_inner:
                        for y in x:
                            result[y] = i
                            i += 1
            if reverse:
                if pos_num >= len(table):
                    origin_result = result
                    result = {}
                    for rank in origin_result:
                        if origin_result[rank] in result:
                            pos = result[origin_result[rank]]
                            result[origin_result[rank]] = pos if pos <= rank else rank
                        else:
                            if rank > len(table):
                                result[origin_result[rank]] = len(table) * 2 + 1 - rank
                            else:
                                result[origin_result[rank]] = rank
                else:
                    if split < 0:
                        rtable = table_outer
                    else:
                        rtable = table_inner
                    origin_result = result
                    result = {}
                    for x in rtable:
                        for rank in x:
                            if origin_result[rank] in result:
                                pos = result[origin_result[rank]]
                                result[origin_result[rank]] = pos if pos <= rank else rank
                            else:
                                if rank > len(table):
                                    result[origin_result[rank]] = len(table) * 2 + 1 - rank
                                else:
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

if __name__ == "__main__":
    print(MatchMaker.position_of_rank_generator(8, (1,6)))

