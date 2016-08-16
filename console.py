'''
Author: Garyuu
Date:   2016/8/14
Name:   console
Descr.: Simple terminal for user.
'''
import controller as Controller
import cmd
import sys

class ScoringConsole(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '-->'
        Controller.initialize()

    def do_exit(self, argstr):
        sys.exit(1)

    def do_reset(self, argstr):
        args = argstr.split()
        if len(args) == 0:
            Controller.reset('all')
        elif len(args) > 1:
            print('Too many arguments.')
        elif args[0] == 'all' or isnumeric(args[0]):
            Controller.reset(args[0])
        else:
            print('The arguments should be numeric or all.')

    def do_hello(self, argstr):
        args = argstr.split()
        if len(args) == 0:
            print('The command should have 1 argument.')
        elif len(args) > 1:
            print('Too many arguments.')
        elif args[0] == 'all' or isnumeric(args[0]):
            Controller.hello(args[0])
        else:
            print('The arguments should be numeric or all.')

    def do_status(self, argstr):
        args = argstr.split()
        if len(args) > 0:
            print('The command should not have any arguments.')
        else:
            Controller.display_status()

    def do_assign(self, argstr):
        args = argstr.split()
        if len(args) < 2:
            print('This command should have at least 2 arguments.')
        elif len(args) > 2:
            print('Too many arguments.')
        elif not (isnumeric(args[0]) and isnumeric(args[1])):
            print('The arguments should be numeric.')
        else:
            Controller.assign(args[0], args[1])

    def do_set(self, argstr):
        args = argstr.split()
        if len(args) < 2:
            print('This command should have at least 2 arguments.')
        else:
            Controller.set(args[0], args[1:])

    def do_setrule(self, argstr):
        args = argstr.split()
        if len(args) == 0:
            print('This command should have 1 arguments.')
        elif len(args) > 1:
            print('Too many arguments.')
        else:
            Controller.setrule(args[0])

    def do_newcontest(self, argstr):
        args = argstr.split()
        if len(args) > 0:
            print('Too many arguments.')
        else:
            Controller.status_clear()

def main():
    c = ScoringConsole()
    c.cmdloop()

if __name__ == '__main__':
    main()
