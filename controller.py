'''
Author: Garyuu
Date:   2016/8/15
Name:   controller
Descr.: The core of the program. It's a bridge to most components.
'''
import configuration
from mqtt_client import MQTTClient
import message_parser as parser
import message_generator as generator
import status
import rule
import threading
from match_maker import MatchMaker
import dbaccess

class Controller:
    def __init__(self):
        self.config = configuration.Config('settings')
        self.load_config()
        self.stage_iter = iter(self.schedule)
        self.current_stage = next(self.stage_iter)
        self.substage = ''

        print("Initializing MQTT client...")
        m_conf = configuration.SectionConfig('settings', 'MQTT')
        self.mqtt = MQTTClient(m_conf)
        self.mqtt.on_message = self.mqtt_on_message
        self.mqtt.connect()

        print("Preparing player data...")
        self.player_list = []
        self.group_dict = {}
        self.load_player_list(self.current_stage + self.substage)
        self.load_waves(self.current_stage + self.substage)
        self.build_group_dict()

        print("Initializing status...")
        self.status = status.Status(self.get_total_number_of_position(), self.current_stage, self.rulename)
        self.status.check = self.all_sent_back_check
        self.status_setstage()
    
    def __del__(self):
        self.destroy()

    #==================#
    # Controll Machine #
    #==================#
    def machine_short_message(self, position, mode):
        msg = {'mode': mode}
        if position != 'all':
            machine_list = [self.status.get_machine_by_position(int(position))]
        else:
            machine_list = self.status.machines

        for machine in machine_list:
            msg['target'] = machine
            self.status.set_position_wait(int(position))
            self.mqtt.publish(generator.gen(msg))

    def machine_reset(self, position):
        self.machine_short_message(position, 'r')

    def machine_hello(self, position):
        self.machine_short_message(position, 'h')

    def machine_force(self, position):
        self.machine_short_message(position, 'f')

    def machine_sleep(self, posision):
        self.machine_short_message(position, 's')

    def machine_wake(self, posision):
        self.machine_short_message(position, 'w', True)

    def machine_assign(self, machine, position):
        if self.status.machines[position] != 0:
            self.status.set_machine_to_position(int(machine), int(position))
        else:
            print("Warning: machine #{} tried to link to position #{},").format(machine, position)
            print("         But the position is already assigned to machine #{}.").format(self.status.machines[position])

    def machine_assign_auto(self):
        self.status.set_machine_auto()

    def machine_unlink(self, position):
        self.status.unlink(int(position))

    def machine_set(self, position):
        if not self.status.position_is_ready(int(position)):
            print("The machine is not ready to receive set messages.")
        else:
            msg = {
                'target'        : self.status.get:_machine_by_position(int(position)),
                'mode'          : str(self.status.rule.machine_mode),
                'wave'          : str(self.status.current_wave),
                'position'      : position,
                'num_players'   : len(self.status.positions[int(position)].player_list),
                'score'         : [],
            }

            for player in self.status.get_player_list_of_position(int(position)):
                msg['score'].append(str(self.status.get_score(player)))
            self.status.set_position_wait(int(position))
            self.mqtt.publish(generator.gen(msg))
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

    def status_nextstage(self):
        if self.status.rule.mode == 'Q' and self.conflict():
            return
        if self.status.rule.mode == 'Q' or self.status.substage == '1': # End of a stage
            self.nextstage_new()
        else: # Move to next round
            self.nextstage_promotion()
        self.load_player_list(self.completed_stage())
        self.build_group_dict()
        self.status.new_stage(self.current_stage, self.substage, self.player_list)

    def status_change_group_position_number(self, group, number):
        if group in self.group_name_list:
            self.config.set('Group', group, number)
            self.build_group_bound()
        else:
            print("There is no group labeled \"{}\".".format(group))

    def status_display(self):
        print(self.status)

    #=========#
    # Methods #
    #=========#
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
        return not (ten_count or x_count)

    def conflict(self):
        for g in self.group_dict:
            plist = list(g['player'])
            while len(plist) > 0:
                tmp = [plist[0]]
                plist.remove(tmp[0])
                for p in plist:
                    if conflict_cmp(tmp[0], p):
                        tmp.append(p)
                        p.remove(tmp[-1])
                if len(tmp) > 1:
                    msg = "Conflict:"
                    for t in tmp:
                        msg += " " + t.tag
                    print(msg)

    def destroy(self):
        self.mqtt.disconnect()

    def mqtt_on_message(self, client, userdata, message):
        self.message_process(parser.parse(message.payload))

    def message_process(self, message):
        print(message)
        if message['type'] == 'ok':
            self.status.set_position_ok(int(message['position']))
        elif message['type'] == 'ready':
            self.status.set_position_ready(int(message['position']))
            self.machine_assign(message['machine'], message['position'])
        elif message['type'] == 'wave':
            self.status.save_wave(message)

    def all_sent_back_check(self, machine):
        msg = {'mode': 'g', 'target': str(machine)}
        self.mqtt.publish(generator.gen(msg))

    def load_config(self):
        self.rulename = self.config.get('Contest', 'standard')
        self.schedule = self.config.get('Contest', 'schedule').split(',')
        self.group_name_list = self.config.get('Contest', 'groups').split(',')

    def load_player_list(self, stage, team_mode=False):
        db_msg = {'action': 'allplayerlist',
                  'stage': stage,
                  'team': team_mode}
        player_data = DBAccess.request(db_msg)
        self.player_list = {}
        for p in player_data:
            self.player_list[p['tag']] = player.Player(p['id'], p['tag'], p['position'], stage, p['group'])
    
    def load_waves(self, stage):
        db_msg = {'action': 'allwavelist',
                  'stage': stage}
        wave_data = DBAccess.request(db_msg)
        for w in wave_data:
            player = self.player_list[w['tag']]
            player.add_wave(w['shot1'], w['shot2'], w['shot3'],
                            w['shot4'], w['shot5'], w['shot6'])
            player.add_score(w['score'])
            player.winner = player.winner or w['winner']

    def load_team_base_score(self, stage):
        db_msg = {'action': 'teamscorelist',
                  'stage': stage}
        score_data = DBAccess.request(db_msg)
        for s in score_data:
            self.player_list[s['t_tag']].add_score(s['score'])

    def build_group_dict(self):
        self.group_dict = {}
        for g in self.group_name_list:
            self.group_dict[g] = {'bound': None, 'players': []}
            for p in self.player_list:
                if p.group == g:
                    self.group_dict[g]['players'].append(p)
        build_group_bound()

    def build_group_bound(self):
        offset = 0
        for g in self.group_name_list:
            size = self.config.getint('Group', g)
            self.group_dict[g]['bound'] = (1+offset, size+offset)
            offset += 1
            
    def get_total_number_of_position(self):
        total = 0
        for group in self.groups:
            total += self.groups[group]
        return total

    def completed_stage(self):
        return self.current_stage+self.substage

    def nextstage_new(self):
        try:
            self.current_stage = next(self.stage_iter)
        except:
            print("Already in end stage.")
            return
        current_rule = rule.Rule(current_stage, self.rulename)
        if current_rule.game_mode == 'D':
            self.substage = 0
            if current_rule.team_size > 1:
                self.load_player_list(current_stage, True)
                self.build_group_dict()
                self.load_team_base_score(current_rule.reference)
            for group in self.group_dict:
                result = MatchMaker.make(group['players'], group['bound'], current_rule.team_size > 1)
                if len(result) > self.substage:
                    self.substage = len(result)
                MatchMaker.send_stage_positions(result, self.current_stage, current_rule.team_size > 1)
            self.substage = str(self.substage)

    def nextstage_promotion(self):
        for group in self.group_dict:
            result = MatchMaker.make(group['players'], group['bound'])
            MatchMaker.send_stage_positions(result, self.current_stage, self.status.rule.team_size)
        self.substage = str(int(self.substage) // 2)
