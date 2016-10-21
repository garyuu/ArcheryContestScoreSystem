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
        self.total_waves = 0
        self.shots_per_wave = 0
        self.win_point = 0
        self.lose_point = 0
        self.draw_point = 0
        self.goal_point = 0
        self.load_stage_rule(stage, rulename)

    def load_stage_rule(self, stage, rulename)
        config = SectionConfig("rules/"+rulename, stage)
        self.machine_mode = config['machinemode']
        self.game_mode = config['mode']
        self.total_waves = config['waves']
        self.shots_per_wave = config['shots']
        self.win_point = config['win']
        self.lose_point = config['lose']
        self.draw_point = config['draw']
        self.goal_point = config['goal']

