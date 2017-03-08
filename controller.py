'''
Author: Garyuu
Date:   2016/8/15
Name:   controller
Descr.: The core of the program. It's a bridge to most components.
'''
import configuration
from tcp_socket import SocketManager
import status
import player
import rule
import threading
import random
from match_maker import MatchMaker
from dbaccess import DBAccess

class Controller:
    def __init__(self):
        self.config = configuration.Config('settings')
        self.group_name_list = []
        self.load_config()
        self.stage_iter = iter(self.schedule)
        self.current_stage = next(self.stage_iter)
        self.substage = ''

        print("Initializing TCP server...")
        self.socket_manager = SocketManager(20000, 40)
        threading.Thread(target = self.message_reader).start()
        self.socket_manager.start()
        
        print("Initializing status...")
        self.status = status.Status(self.get_total_number_of_position(), self.rulename)
        self.status.check = self.all_sent_back_check
        while self.current_stage != self.status.stage:
            self.current_stage = next(self.stage_iter)
        self.substage = self.status.substage
    
        print("Reload player data...")
        self.player_list = []
        self.player_list_tag_index = []
        self.group_dict = {}
        self.load_player_list(self.current_stage + self.substage)
        self.load_waves(self.current_stage + self.substage)
        self.build_group_dict()
        self.status.player_list = self.player_list
        self.status.build_position_list()

    def __del__(self):
        #self.destroy()
        pass

    #==================#
    # Controll Machine #
    #==================#
    def machine_short_message(self, position, command):
        msg = {'command': command}
        if position != 'all':
            machine_list = [self.status.positions[(int(position))].machine]
        else:
            machine_list = self.status.machines

        for machine in machine_list:
            if machine > 0:
                msg['machine'] = machine
                self.status.set_position_wait(int(position))
                self.socket_manager.send(msg)

    def machine_reset(self, position):
        if position == 'all':
            for i in range(1, self.get_total_number_of_position()):
                self.machine_short_message(i, 'reset')
        else:
            self.machine_short_message(position, 'reset')

    def machine_force(self, position):
        if position == 'all':
            for i in range(1, self.get_total_number_of_position()):
                self.machine_short_message(i, 'force')
        else:
            self.machine_short_message(position, 'force')

    def machine_sleep(self, position):
        if position == 'all':
            for i in range(1, self.get_total_number_of_position()):
                self.machine_short_message(i, 'sleep')
        else:
            self.machine_short_message(position, 'sleep')

    def machine_assign(self, machine, position):
        if self.status.machines[position] == 0:
            self.status.set_machine_to_position(int(machine), int(position))
        elif self.status.machines[position] != machine:
            print("Warning: machine #{} tried to link to position #{},".format(machine, position))
            print("         But the position is already assigned to machine #{}.".format(self.status.machines[position]))

    def machine_assign_auto(self):
        self.status.set_machine_auto()

    def machine_unlink(self, position):
        self.status.unlink(int(position))

    def machine_set(self, position):
        if not self.status.position_is_ready(int(position)):
            print("Position {} is not ready to receive set messages.".format(position))
        elif self.status.need_to_be_set(position):
            msg = {
                'machine'       : self.status.positions[(int(position))].machine,
                'command'       : 'setwave',
                'wave'          : str(self.status.current_wave),
                'position'      : position,
                'shots'         : str(self.status.rule.shots_per_wave),
                'num_players'   : len(self.status.positions[int(position)].players),
                'players'       : [],
                'scores'        : [],
            }
            for player in self.status.positions[int(position)].players:
                msg['players'].append(player.tag)
                msg['scores'].append(player.total_score())

            self.status.set_position_wait(int(position))
            self.socket_manager.send(msg)
            self.status.set_position_receiving(int(position))
    
    #=================#
    # Controll Status #
    #=================#
    def status_setrule(self, rulename):
        self.status.set_rulename(rulename)

    def status_clear(self):
        self.status.clear()

    def status_nextwave(self):
        self.status.next_wave()
        for i in range(1, self.get_total_number_of_position()+1):
            self.machine_set(i)

    def status_nextstage(self):
        if self.status.rule.game_mode == 'Q' and self.conflict():
            return
        if self.status.rule.game_mode == 'P' or self.status.rule.game_mode == 'Q' or self.status.substage == '1': # End of a stage
            self.nextstage_new()
        else: # Move to next round
            self.nextstage_promotion()
        self.load_player_list(self.completed_stage())
        self.build_group_dict()
        self.status.new_stage(self.current_stage, self.substage, self.player_list)

    def status_change_group_position_number(self, group, number):
        if group in self.group_name_list:
            self.config.set('Group', group, str(number))
            self.build_group_bound()
        else:
            print("There is no group labeled \"{}\".".format(group))

    def status_display(self, pos=0):
        if pos:
            print(self.status.positions[pos])
        else:
            print("Group")
            for g in self.group_name_list:
                print("{}: {} ".format(g, self.config.get('Group', g)))
            print(self.status)

    def status_conflict_solve(self, tag, win):
        player = self.get_player_by_tag(tag)
        player.winner = win
        player.send_winner_change()

    #=========#
    # Methods #
    #=========#
    def random_conflict_solver(self, conlist):
        c = list(conlist)
        random.shuffle(c)
        while len(c) > 1:
            c[0].winner = len(c) - 1
            c[0].send_winner_change()
            c.remove(c[0])

    def is_promote_rank(self, plist, player):
        promote_num = len(plist)
        while promote_num & (-promote_num) != promote_num: #if promote is not 2**k, turn into 2**k
            promote_num -= promote_num & (-promote_num)
        count = 0
        for p in plist:
            if p.total_score() > player.total_score():
                count += 1
        return count == promote_num

    def conflict_cmp(self, a, b):
        if a.total_score != b.total_score:
            return False
        ten_count = 0
        x_count = 0
        for i in a.wave_list:
            for j in i:
                if j >= 10:
                    ten_count += 1
                if j > 10:
                    x_count += 1
        for i in b.wave_list:
            for j in i:
                if j >= 10:
                    ten_count -= 1
                if j > 10:
                    x_count -= 1
        return not (ten_count or x_count or a.winner or b.winner)

    def conflict(self):
        conflict_flag = False
        for g in self.group_dict:
            plist = list(self.group_dict[g]['players'])
            while len(plist) > 0:
                # Build conflict group
                # and remove players with the same score from list
                con = [plist[0]]
                plist.remove(con[0])
                for p in plist:
                    if self.conflict_cmp(con[0], p):
                        con.append(p)
                        p.remove(con[-1])
                # If conflict group has more than 1 person
                if len(con) > 1:
                    if self.is_promote_rank(g['players'], con[0]):
                        msg = "Promote conflict in group [{}]:".format(g)
                        for t in con:
                            msg += " " + t.tag
                        print(msg)
                        conflict_flag = True
                    else:
                        self.random_conflict_solver(con)
        return conflict_flag

    def destroy(self):
        pass

    def message_reader(self):
        while True:
            message = self.socket_manager.pop_message()
            if message:
                self.message_process(message)

    def message_process(self, message):
        print(message)
        if 'position' in message:
            pos = message['position']
        else:
            pos = self.status.machines.index(message['machine'])
        if message['command'] == 'response':
            self.status.set_position_ok(pos)
        elif message['command'] == 'initialize':
            self.status.set_position_ready(pos)
            self.machine_assign(int(message['machine']), pos)
            resp = {'machine': int(message['machine']), 'command': 'response', 'status': True}
            self.socket_manager.send(resp)
        elif message['command'] == 'sendwave':
            self.status.save_wave(message)

    def all_sent_back_check(self, machine):
        msg = {'command': 'response', 'machine': str(machine), 'status': True}
        self.socket_manager.send(msg)

    def load_config(self):
        self.rulename = self.config.get('Contest', 'rulename')
        self.schedule = self.config.get('Contest', 'schedule').split(',')
        self.group_name_list = self.config.get('Contest', 'groups').split(',')

    def load_player_list(self, stage, team_mode=False):
        db_msg = {'action': 'allplayerlist',
                  'stage': stage,
                  'team': team_mode}
        player_data = DBAccess.request(db_msg)['content']
        self.player_list = []
        for p in player_data:
            self.player_list_tag_index.append(p['tag'])
            self.player_list.append(player.Player(int(p['id']), p['tag'], int(p['position']), p['stage'], p['groupname'], p['rank']))
    
    def load_waves(self, stage):
        db_msg = {'action': 'allwavelist',
                  'stage': stage}
        wave_data = DBAccess.request(db_msg)['content']
        for w in wave_data:
            player = self.get_player_by_tag(w['tag'])
            player.add_wave(int(w['shot1']), int(w['shot2']), int(w['shot3']),
                            int(w['shot4']), int(w['shot5']), int(w['shot6']))
            player.add_score(int(w['score']))
            player.winner = player.winner or int(w['winner'])

    def load_team_base_score(self, stage):
        db_msg = {'action': 'teamscorelist',
                  'stage': stage}
        score_data = DBAccess.request(db_msg)
        for s in score_data:
            self.player_list[s['t_tag']].add_score(s['score'])
    
    def get_player_by_tag(self, tag):
        return self.player_list[self.player_list_tag_index.index(tag)]

    def build_group_dict(self):
        self.group_dict = {}
        for g in self.group_name_list:
            self.group_dict[g] = {'bound': None, 'players': []}
            for p in self.player_list:
                if p.group == g:
                    self.group_dict[g]['players'].append(p)
        self.build_group_bound()

    def build_group_bound(self):
        offset = 0
        for g in self.group_name_list:
            size = self.config.getint('Group', g)
            self.group_dict[g]['bound'] = (1+offset, size+offset)
            offset += 1
            
    def get_total_number_of_position(self):
        total = 0
        for group in self.group_name_list:
            total += self.config.getint('Group', group)
        return total

    def completed_stage(self):
        return self.current_stage+self.substage

    def nextstage_new(self):
        try:
            self.current_stage = next(self.stage_iter)
        except:
            print("Already in end stage.")
            return
        current_rule = rule.Rule(self.current_stage, self.rulename)
        if current_rule.game_mode == 'D':
            self.substage = 0
            if current_rule.team_size > 1:
                self.load_player_list(current_stage, True)
                self.build_group_dict()
                self.load_team_base_score(current_rule.reference)
            for g in self.group_dict:
                group = self.group_dict[g]
                if len(group['players']) == 0:
                    continue
                pos_size = group['bound'][1] - group['bound'][0] + 1
                pmt_size = len(group['players'])
                while pmt_size & -pmt_size != pmt_size:
                    pmt_size -=  pmt_size & -pmt_size
                split = pos_size * 2 < pmt_size
                result = MatchMaker.make(group['players'], g, True, split)
                if len(result) > self.substage:
                    self.substage = len(result)
                MatchMaker.send_stage_positions(result, self.current_stage, current_rule.team_size > 1)
            self.substage = str(self.substage)

    def nextstage_promotion(self):
        for g in self.group_dict:
            group = self.group_dict[g]
            if len(group['players']) == int(self.substage):
                result = MatchMaker.make(group['players'], g)
                MatchMaker.send_stage_positions(result, self.current_stage, self.status.rule.team_size)
            else:
                result = MatchMaker.make(group['players'], g, False, True)
                MatchMaker.send_stage_positions(result, self.current_stage, self.status.rule.team_size, True)
        self.substage = str(int(self.substage) // 2)
