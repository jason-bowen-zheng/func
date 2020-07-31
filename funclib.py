# func/funclib.py
# func runtime lib

try:
    import readline
except:
    print("func: No 'readline' found")
import shlex
import string
import sympy as sym
import sympy.abc as var
import sys

class core(object):

    def __init__(self):
        self.var = {}
        self.function = {
                    'ipf': ipf,
                    'lf' : lf,
                    'ppf': ppf,
                }
        self.version = '0.1'

    def def_(self, type_, name, *args):
        if name in string.ascii_letters:
            if type_ in self.function:
                self.var[name] = self.function[type_](*args)
                print(name, '=', self.var[name])
            else:
                raise TypeError("No function type: '%s'" % type_)
        else:
            raise TypeError("Invalid name: '%s'" % name)

    def getq(self, name):
        print('In', ', '.join([str(item) for item in self.var[name].getq()]), 'quadrants')

    def getx(self, name, y):
        print('x =', self.var[name].getx(y))

    def gety(self, name, x):
        print('y =', self.var[name].gety(x))

    def ls(self):
        for k, v in self.var.items():
            print(k, '=', str(v))

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
                    elif cmd[0] == 'def':
                        self.def_(*cmd[1:])
                    elif cmd[0] == 'getq':
                        self.getq(*cmd[1:])
                    elif cmd[0] == 'getx':
                        self.getx(*cmd[1:])
                    elif cmd[0] == 'gety':
                        self.gety(*cmd[1:])
                    elif cmd[0] == 'ls':
                        self.ls(*cmd[1:])
                    elif cmd[0] == 'quit':
                        self.quit(*cmd[1:])
                    elif cmd[0] == 'undef':
                        self.undef(*cmd[1:])
                    else:
                        print("func: Command not found:", cmd[0])
                except Exception as err:
                    print('func:', str(err))
                else:
                    pass

    def quit(self, code=0):
        sys.exit(int(code))

    def undef(self, *names):
        for name in names:
            del self.var[name]

# class of functions

class ipf(object):
    # Inverse proportional function

    def __init__(self, *args):
        # ipf <k>
        # ipf <x> <y>
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

    def __str__(self):
        return 'ipf(' + str(self.k) + ')'

    def getq(self):
        if self.k > 0:
            return [1, 3]
        elif self.k < 0:
            return [2, 4]

    def getx(self, y):
        return self.k / float(y)

    def gety(self, x):
        return self.k / float(x)

class lf(object):
    # Linear function
        
    def __init__(self, *args):
        # lf <k> <b>
        # lf <x1> <y1> <x2> <y2>
        if len(args) == 2:
            if (num := float(args[0])) != 0:
                self.k = float(args[0])
            else:
                raise TypeError("'x' cannot equals to 0")
            self.b = float(args[1])
        elif len(args) == 4:
            x1, y1 = float(args[0]), float(args[1])
            x2, y2 = float(args[2]), float(args[3])
            eq1 = sym.Eq(var.k * x1 + var.b, y1)
            eq2 = sym.Eq(var.k * x2 + var.b, y2)
            ans = sym.solve([eq1, eq2], [var.k, var.b])
            self.k, self.b = ans[var.k], ans[var.b]
        else:
            raise TypeError("Function 'lf' needs 2 or 4 arguments but %d found" % len(args))
    
    def __str__(self):
        return 'lf(' + str(self.k) + ', ' + str(self.b) +  ')'

    def getq(self):
        quadrant = []
        if self.k > 0:
            quadrant += [1, 3]
            if self.b > 0:
                quadrant += [2]
            elif self.b < 0:
                quadrant += [4]
            else:
                pass
        elif self.k < 0:
            quadrant += [2, 4]
            if self.b > 0:
                quadrant += [3]
            elif self.b < 0:
                quadrant += [1]
            else:
                pass
        else:
            pass
        return quadrant

    def getx(self, y):
        return (float(y) - self.b) / self.k

    def gety(self, x):
        return self.k * float(x) + self.b
	
	
class ppf(object):
    # Positive proportional function

    def __init__(self, *args):
        # ppf <k>
        # ppf <x> <y>
        if len(args) == 1:
            if (num := float(args[0])) != 0:
                self.k = num
            else:
                raise TypeError("'k' cannot equals to 0")
        elif len(args) == 2:
            if float(args[0]) != 0:
                self.k = float(args[1]) / float(args[0])
            else:
                raise TypeError("'x' cannot equals to 0")
        else:
            raise TypeError("Function 'ppf' needs 1 to 2 arguments but %d found" % len(args))

    def __str__(self):
        return 'ppf(' + str(self.k) + ')'

    def getq(self):
        if self.k > 0:
            return [1, 3]
        elif self.k < 0:
            return [2, 4]

    def getx(self, y):
        return float(y) / self.k

    def gety(self, x):
        return self.k * float(x)

