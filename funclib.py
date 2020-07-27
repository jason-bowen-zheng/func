# func/funclib.py
# func runtime lib

try:
    import readline
except:
    print("func: No 'readline' found")
import shlex
import string
import sys

class core(object):

    def __init__(self):
        self.var = {}
        self.function = {
                    'ipf': ipf,
                }
        self.version = '0.1'

    def define(self, type_, name, *args):
        if name in string.ascii_letters:
            if type_ in self.function:
                self.var[name] = self.function[type_](*args)
                print(self.var[name])
            else:
                raise TypeError("No function type: '%s'" % type_)
        else:
            raise TypeError("Invalid name: '%s'" % name)

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


class ipf(object):
    # Inverse proportional function

    def __init__(self, *args):
        if len(args) == 1:
            if (num := float(args[0])) != 0:
                self.k = num
            else:
                raise TypeError("'k' cannot equals to 0")
        elif len(args) == 2:
            if (num := float(args[0]) * float(args[1])) != 0:
                self.k = num
            else:
                raise TypeError("'k' cannot equals to 0")
        else:
            raise TypeError("Function 'ipf' needs 1 to 2 arguments but %d found" % len(args))

    def getx(self, y):
        return self.k / float(y)

    def gety(self, x):
        return self.k / float(x)
