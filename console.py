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

    def do_exit(self, argstr):
        self.ctrl.destroy()
        sys.exit(1)

    def do_reset(self, argstr):
        args = argstr.split()
        if len(args) == 0:
            print('The command should have 1 argument.')
        elif len(args) > 1:
            print('Too many arguments.')
        elif args[0] == 'all' or args[0].isnumeric():
            self.ctrl.machine_reset(args[0])
        else:
            print('The argument should be numeric or all.')

    def do_hello(self, argstr):
        args = argstr.split()
        if len(args) == 0:
            print('The command should have 1 argument.')
        elif len(args) > 1:
            print('Too many arguments.')
        elif args[0] == 'all' or args[0].isnumeric():
            self.ctrl.machine_hello(args[0])
        else:
            print('The argument should be numeric or all.')

    def do_force(self, argstr):
        args = argstr.split()
        if len(args) < 1:
            print('This command should have at least 1 argument.')
        elif len(args) > 1:
            print('Too many arguments.')
        elif args[0] == 'all' or args[0].isnumeric():
            self.ctrl.machine_force(args[0])
        else:
            print('The argument should be numeric or all.')

    def do_status(self, argstr):
        args = argstr.split()
        if len(args) > 0:
            print('The command should not have any arguments.')
        else:
            self.ctrl.status_display()

    def do_assign(self, argstr):
        args = argstr.split()
        if len(args) < 2:
            print('This command should have at least 2 arguments.')
        elif len(args) > 2:
            print('Too many arguments.')
        elif not (args[0].isnumeric() and args[1].isnumeric()):
            print('The arguments should be numeric.')
        else:
            self.ctrl.machine_assign(args[0], args[1])

    def do_set(self, argstr):
        args = argstr.split()
        if len(args) < 1:
            print('This command should have at least 1 argument.')
        elif len(args) > 1:
            print('Too many arguments.')
        else:
            self.ctrl.machine_set(args[0])

    def do_setrule(self, argstr):
        args = argstr.split()
        if len(args) == 0:
            print('This command should have 1 arguments.')
        elif len(args) > 1:
            print('Too many arguments.')
        else:
            self.ctrl.status.setrule(args[0])

    def do_newcontest(self, argstr):
        args = argstr.split()
        if len(args) > 0:
            print('Too many arguments.')
        else:
            self.ctrl.status_clear()

    def do_nextwave(self, argstr):
        self.ctrl.status_nextwave()

def main():
    c = ScoringConsole()
    c.cmdloop()

if __name__ == '__main__':
    main()
