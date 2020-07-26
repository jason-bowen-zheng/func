# func/funclib.py
# func runtime lib

try:
    import readline
except:
    print("func: No 'readline' found")
import shlex
import sys

class core(object):

    def __init__(self):
        self.function = {}
        self.version = '0.1'

    def define(self, name):
        pass

    def run(self):
        print('func %s' % self.version)
        print('Copyright (c) Jason Zheng 2020.')
        print('All Right Reserved.')
        while True:
            try:
                cmd = input('> ')
            except KeyboardInterrupt:
                print('\nfunc: Interrupt')
            except EOFError:
                print('\nfunc: Stop')
                sys.exit(1)
            else:
                try:
                    cmd = shlex.split(cmd)
                    if cmd == []:
                        pass
                    elif cmd[0] == 'define':
                        self.define(*cmd[1:])
                    elif cmd[0] == 'quit':
                        self.quit(*cmd[1:])
                    else:
                        print("func: Command not found:", cmd[0])
                except Exception as err:
                    print('func:', str(err))
                else:
                    pass

    def quit(self, code=0):
        sys.exit(int(code))
