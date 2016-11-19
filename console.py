'''
Author: Garyuu
Date:   2016/8/14
Name:   console
Descr.: Simple terminal for user.
'''
from controller import Controller
import cmd
import sys

class ScoringConsole(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '-->'
        self.ctrl = Controller()
        self.args = []

    def parse(self, line, arg_num):
        self.args = line.split()
        if len(self.args) < arg_num:
            print('Need at least {} arguments.'.format(arg_num))
        elif len(self.args) > arg_num:
            print('Too many argument! At most {} arguments.'.format(arg_num))
        else:
            return True
        return False

    def do_exit(self, argstr):
        if self.parse(argstr, 0):
            self.ctrl.destroy()
            sys.exit(1)

    def do_reset(self, argstr):
        if self.parse(argstr, 1):
            try:
                self.ctrl.machine_reset(int(self.args[0]))
            except ValueError:
                print("The argument should be numeric.")
    
    def do_resetall(self, argstr):
        if self.parse(argstr, 0):
            self.ctrl.machine_reset('all')

    def do_hello(self, argstr):
        if self.parse(argstr, 1):
            try:
                self.ctrl.machine_hello(int(self.args[0]))
            except ValueError:
                print("The argument should be numeric.")

    def do_helloall(self, argstr):
        if self.parse(argstr, 0):
            self.ctrl.machine_hello('all')

    def do_force(self, argstr):
        if self.parse(argstr, 1):
            try:
                self.ctrl.machine_force(int(self.args[0]))
            except ValueError:
                print("The argument should be numeric.")

    def do_forceall(self, argstr):
        if self.parse(argstr, 0):
            self.ctrl.machine_force('all')

    def do_sleep(self, argstr):
        if self.parse(argstr, 2):
            try:
                self.ctrl.machine_sleep(int(self.args[0]), int(self.args[1]))
            except ValueError:
                print("The argument should be numeric.")

    def do_sleepall(self, argstr):
        if self.parse(argstr, 1):
            try:
                self.ctrl.machine_sleep('all', int(self.args[0]))
            except ValueError:
                print("The argument should be numeric.")

    def do_wake(self, argstr):
        if self.parse(argstr, 1):
            try:
                self.ctrl.machine_wake(int(self.args[0]))
            except ValueError:
                print("The argument should be numeric.")

    def do_wakeall(self, argstr):
        if self.parse(argstr, 0):
            self.ctrl.machine_wake('all')

    def do_status(self, argstr):
        if self.parse(argstr, 0):
            self.ctrl.status_display()

    def do_statuspos(self, argstr):
        if self.parse(argstr, 1):
            try:
                self.ctrl.status_display(int(self.args[0]))
            except ValueError:
                print("The argument should be numeric.")

    def do_assign(self, argstr):
        if self.parse(argstr, 2):
            try:
                self.ctrl.machine_assign(int(self.args[0]), int(self.args[1]))
            except ValueError:
                print("All arguments should be numeric.")

    def do_unlink(self, argstr):
        if self.parse(argstr, 1):
            try:
                self.ctrl.machine_unlink(int(self.args[0]))
            except ValueError:
                print("The argument should be numeric.")

    def do_setwave(self, argstr):
        if self.parse(argstr, 1):
            try:
                self.ctrl.machine_set(int(self.args[0]))
            except ValueError:
                print("The argument should be numeric.")

    def do_nextwave(self, argstr):
        if self.parse(argstr, 0):
            self.ctrl.status_nextwave()

    def do_changestage(self, argstr):
        if self.parse(argstr, 0):
            self.ctrl.status_nextstage()

    def do_positionchange(self, argstr):
        if self.parse(argstr, 2):
            try:
                self.ctrl.status_change_group_position_number(self.args[0], int(self.args[1]))
            except ValueError:
                print("Argument 1 should be groupname. Argument 2 should be numeric.")

    def do_conflictsolve(self, argstr):
        if self.parse(argstr, 2):
            try:
                self.ctrl.status_conflict_solve(self.args[0], int(self.args[1]))
            except ValueError:
                print("Argument 1 should be tag. Argument 2 should be numeric.")

    def do_reloadplayerdata(self, argstr):
        if self.parse(argstr, 0):
            self.ctrl.load_player_list()
            self.ctrl.load_waves()

def main():
    c = ScoringConsole()
    c.cmdloop()

if __name__ == '__main__':
    main()
