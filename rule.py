'''
Author: Garyuu
Date:   2016/10/17
Name:   rule
Descr.: Load rule of the stage assigned.
'''

from configuration import SectionConfig

class Rule:
    def __init__(self, stage, rulename):
        self.machine_mode = 0
        self.game_mode = ''
        self.reference = None
        self.team_size = 0
        self.total_waves = 0
        self.shots_per_wave = 0
        self.win_point = 0
        self.lose_point = 0
        self.draw_point = 0
        self.goal_point = 0
        self.load_stage_rule(stage, rulename)

    def load_stage_rule(self, stage, rulename):
        config = SectionConfig("rules/"+rulename, stage)
        self.machine_mode = int(config['modeid'])
        self.game_mode = config['mode']
        self.reference = config['reference']
        self.team_size = int(config['team'])
        self.total_waves = int(config['waves'])
        self.shots_per_wave = int(config['shots'])
        self.win_point = int(config['win'])
        self.lose_point = int(config['lose'])
        self.draw_point = int(config['draw'])
        self.goal_point = int(config['goal'])

