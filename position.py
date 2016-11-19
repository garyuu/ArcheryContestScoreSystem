'''
Author: NekOrz, Garyuu
Date:   2016/8/15
Name:   position
Descr.: The object that serves as a signal/timer thingy
'''
import threading
import math
from enum import Enum

class StateEnum(Enum):
    Empty = -1
    Idle = 0
    Ready = 1
    Sleeping = 2
    Received = 3
    Receiving = 4

class Position():
    def __init__(self, pid, mid):
        self.id = pid
        self.machine = mid
        self.players = []
        self.state = StateEnum.Empty
        self.waiting = False
        self.dead = False

    def __str__(self):
        output = self.line_status() + "\n"
        for p in self.players:
            output += str(p) + "\n"
        return output

    def line_status(self):
        dead = 'X' if self.dead else ' '
        return "{:>2}:M{}:[{}], {}-P{}".format(self.id, self.machine, dead, self.state.name, self.player_number())

    def player_number(self):
        return len(self.players)

    def change_state(self, state):
        self.state = StateEnum[state]

    def save_wave(self, tag, shots):
        for p in self.players:
            if p.tag == tag:
                p.add_wave_from_list(shots)
                p.latest_wave_sum()

    def calculate_score(self, rule):
        if rule.game_mode == 'D':
            if self.players[0].wave_count() <= rule.total_waves:
                #  Assume that each dual match has only 2 players/teams.
                if self.players[0].score_list[-1] > self.players[1].score_list[-1]:
                    self.players[0].score_list[-1] = rule.win_point
                    self.players[1].score_list[-1] = rule.lose_point
                elif self.players[0].score_list[-1] < self.players[1].score_list[-1]:
                    self.players[1].score_list[-1] = rule.win_point
                    self.players[0].score_list[-1] = rule.lose_point
                else:
                    self.players[0].score_list[-1] = rule.draw_point
                    self.players[1].score_list[-1] = rule.draw_point
                if self.players[0].total_score() == rule.goal_point:
                    self.players[0].winner = True
                if self.players[1].total_score() == rule.goal_point:
                    self.players[1].winner = True
            else:
                if self.players[0].score_list[-1] > self.players[1].score_list[-1]:
                    self.players[0].winner = True
                else:
                    self.players[1].winner = True
                self.players[0].score_list[-1] = 0
                self.players[1].score_list[-1] = 0
            self.players[0].latest_wave_save()
            self.players[1].latest_wave_save()
        else:
            for p in self.players:
                p.latest_wave_save()

    def wait_for_response(self,sec = 10.0):
        self.waiting = True
        self.timer = threading.Timer(sec,self.set_dead)
        self.timer.start()
        
    def set_dead(self):
        self.dead = True
    
    def received_response(self):
        self.timer.cancel()
        self.waiting = False
        self.dead = False
    
    def all_back(self, wave):
        for p in self.players:
            if p.wave_count() != wave:
                return False
        return True

    def is_ready(self):
        return self.state == StateEnum.Ready

    def has_winner(self):
        return self.players[0].winner or self.players[1].winner

    def clear_player_data(self):
        # TODO Method to clear all players' data in this position.
        pass
        
def main():
    pass
    
if __name__ == '__main__':
    main()
