#!/usr/bin/env python3

import math
from os import path, linesep
try:
    import readline
except:
    pass
import shlex
import sympy as sym
import sympy.abc as var
from sympy.core.numbers import Integer, Float
import sys

usage_str = {
        'def': 'Define a function: def <function> <name> [arg...]',
        'undef': 'Delete functions: undef <name...>',
        'ls': 'List functions: ls <f|t>',
        'getx': 'Get x-axis value: getx <name> <y>',
        'gety': 'Get y-axis value: gety <name> <x>',
        'getip': 'Get point of intersection: getip <name1> <name2>',
        'set': 'Set function attributes: set <name>.<attribute> <value>',
        'save': 'Save functions to file: save [*.func file]',
        'load': 'Load functions from file: load [*.func file]',
        'using': 'Import extra functions: using <*.py file>',
        'plot': 'Draw plot: plot <name>'
    }


class core(object):

    def __init__(self):
        self.var = {}
        self.function = {
                    'cvf': cvf,
                    'ipf': ipf,
                    'lf' : lf ,
                    'ppf': ppf,
                    'qf' : qf
                }
        self.version = '0.1'

    def def_(self, type_, name, *args):
        if ' ' not in name:
            if type_ in self.function:
                [float(sym.sympify(item)) for item in args]
                self.var[name] = self.function[type_](*[sym.sympify(item) for item in args])
                print(name, '=', self.var[name])
            else:
                raise TypeError("No function type: '%s'" % type_)
        else:
            raise TypeError('Invalid name')

    def getip(self, f1, f2):
        ans = sym.solve([self.var[f1].geteq(), self.var[f2].geteq()], [var.x, var.y])
        if isinstance(ans, list):
            for item in ans:
                print(item)
        elif isinstance(ans, dict):
            print('(%s, %s)' % (ans[var.x], ans[var.y]))

    def getq(self, name):
        print('In', ', '.join([str(item) for item in self.var[name].getq()]), 'quadrants')

    def getx(self, name, y):
        print('x =', self.var[name].getx(sym.sympify(y)))

    def gety(self, name, x):
        print('y =', self.var[name].gety(sym.sympify(x)))

    def set(self, attribute, value):
        if '.' in attribute:
            name, attribute = attribute.split('.', 1)
        else:
            raise TypeError("Use '.'(dot) to split function and attribute")
        if hasattr(self.var[name], attribute):
            if isinstance(getattr(self.var[name], attribute), (int, float, Integer, Float)):
                float(sym.sympify(value))
                setattr(self.var[name], attribute, sym.sympify(value))
                print(name, '=', self.var[name])
            else:
                raise TypeError("Not a number object: '%s'" % attribute)
        else:
            raise TypeError("No attribute: '%s'" % attribute)

    def save(self, name='default.func'):
        with open(name, 'w+') as f:
            for k, v in self.var.items():
                f.write('%s = %s%s' % (k, v, linesep))

    def load(self, name='default.func'):
        if path.isfile(name):
            with open(name, 'r+') as f:
                for line in f.readlines():
                    line = line.strip()
                    type_ = line[line.find('=') + 1: line.find('(')].strip()
                    name = line[:line.find('=')].strip()
                    arg = [i[i.find('=') + 1:] for i in [i.strip() for i in line[line.find('(') + 1: -1].split(',')]]
                    self.def_(type_, name, *arg)
        else:
            raise TypeError("File '%s' not found" % name)

    def ls(self, type_='f'):
        if type_ == 'f':
            i = 1
            for k, v in self.var.items():
                print('%s) %s = %s' % (str(i).rjust(len(str(len(self.var))), ' '), k, str(v)))
                i += 1
        elif type_ == 't':
            i = 1
            for item in self.function:
                print('%s) %s' % (str(i).rjust(len(str(len(self.function))), ' '), item))
                i += 1
        else:
            raise TypeError("No subcommand : '%s'" % type_)

    def plot(self, f):
        self.var[f].plot()

    def quit(self, code=0):
        sys.exit(int(code))

    def run(self):
        print('func %s for %s' % (self.version, sys.platform))
        print("Type 'usage' for help, 'quit' to exit")
        while True:
            try:
                cmd = input('>>> ')
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
                    elif cmd[0] == 'getip':
                        self.getip(*cmd[1:])
                    elif cmd[0] == 'getq':
                        self.getq(*cmd[1:])
                    elif cmd[0] == 'getx':
                        self.getx(*cmd[1:])
                    elif cmd[0] == 'gety':
                        self.gety(*cmd[1:])
                    elif cmd[0] == 'set':
                        self.set(*cmd[1:])
                    elif cmd[0] == 'ls':
                        self.ls(*cmd[1:])
                    elif cmd[0] == 'save':
                        self.save(*cmd[1:])
                    elif cmd[0] == 'load':
                        self.load(*cmd[1:])
                    elif cmd[0] == 'plot':
                        self.plot(*cmd[1:])
                    elif cmd[0] == 'quit':
                        self.quit(*cmd[1:])
                    elif cmd[0] == 'usage':
                        self.usage(*cmd[1:])
                    elif cmd[0] == 'undef':
                        self.undef(*cmd[1:])
                    elif cmd[0] == 'using':
                        self.using(*cmd[1:])
                    else:
                        print("func: Command not found:", cmd[0])
                except Exception as err:
                    print('func: error:', str(err))
                else:
                    pass

    def usage(self, topic=''):
        if topic in usage_str:
            print("Usage on '%s':" % topic)
            desp, usage = usage_str[topic].split('; ', 1)
            print('  Description: %s' % desp)
            print('  Usage      : %s' % usage)
        elif not topic:
            print('Usage on all commands:')
            for cmd, desp in usage_str.items():
                length = max([len(s) for s in usage_str.keys()])
                print('  %s: %s' % (cmd + ' ' * (length - len(cmd)), desp.split(': ')[1]))
        elif topic not in usage_str:
            raise TypeError("No usage topic '%s' found" % topic)

    def undef(self, *names):
        for name in names:
            del self.var[name]

    def using(self, lib):
        lib = __import__(lib)
        count = 0
        for item in [name for name in dir(lib) if not name.startswith('_')]:
            name, f = item, getattr(lib, item)
            if isinstance(f, object):
                if hasattr(f, 'geteq') and hasattr(f, 'getx') and hasattr(f, 'gety') and hasattr(f, 'plot'):
                    self.function[name] = f
                    count += 1
        else:
            print('Total load %d functions' % count)


class cvf(object):
    # Constant value function

    def __init__(self, *args):
        if len(args) == 1:
            if float(args[0]) != 0:
                self.c = args[0]
            else:
                raise TypeError("'c' cannot equals to 0")
        else:
            raise TypeError("Funcation 'cvf' takes 1 argument but %d given" % len(args))

    def __str__(self):
        return 'cvf(c=%s)' % self.c

    def geteq(self):
        return sym.Eq(self.c, var.y)

    def getq(self):
        if self.c > 0:
            return [1, 2]
        elif self.c < 0:
            return [3, 4]

    def getx(self, y):
        pass

    def gety(self, x):
        return self.c

    def plot(self):
        sym.plotting.plot(self.c)


class ipf(object):
    # Inverse proportional function

    def __init__(self, *args):
        if len(args) == 1:
            if float(args[0]) != 0:
                self.k = args[0]
            else:
                raise TypeError("'k' cannot equals to 0")
        elif len(args) == 2:
            if float(args[0]) * float(args[1]) != 0:
                self.k = args[0] * args[1]
            else:
                raise TypeError("'k' cannot equals to 0")
        else:
            raise TypeError("Function 'ipf' takes 1 to 2 arguments but %d given" % len(args))

    def __str__(self):
        return 'ipf(k=%s)' % self.k

    def geteq(self):
        return sym.Eq(self.k / var.x, var.y)

    def getq(self):
        if self.k > 0:
            return [1, 3]
        elif self.k < 0:
            return [2, 4]

    def getx(self, y):
        return self.k / y

    def gety(self, x):
        return self.k / x

    def plot(self):
        sym.plotting.plot(self.k / var.x)


class lf(object):
    # Linear function
        
    def __init__(self, *args):
        if len(args) == 2:
            if float(args[0]) != 0:
                self.k = args[0]
                self.b = args[1]
            else:
                raise TypeError("'x' cannot equals to 0")
        elif len(args) == 4:
            x1, y1 = args[0], args[1]
            x2, y2 = args[2], args[3]
            eq1 = sym.Eq(var.k * x1 + var.b, y1)
            eq2 = sym.Eq(var.k * x2 + var.b, y2)
            ans = sym.solve([eq1, eq2], [var.k, var.b])
            if ans[var.k] == 0:
                raise TypeError("'k' cannot equals to 0")
            else:
                self.k, self.b = ans.values()
        else:
            raise TypeError("Function 'lf' takes 2 or 4 arguments but %d given" % len(args))
    
    def __str__(self):
        return 'lf(k=%s, b=%s)' % (self.k, self.b)

    def geteq(self):
        return sym.Eq(self.k * var.x + self.b, var.y)

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
        return (y - self.b) / self.k

    def gety(self, x):
        return self.k * x + self.b

    def plot(self):
        sym.plotting.plot(self.k * var.x + self.b)


class ppf(object):
    # Positive proportional function

    def __init__(self, *args):
        if len(args) == 1:
            if float(args[0]) != 0:
                self.k = args[0]
            else:
                raise TypeError("'k' cannot equals to 0")
        elif len(args) == 2:
            if float(args[0]) != 0:
                self.k = args[1] / args[0]
            else:
                raise TypeError("'x' cannot equals to 0")
        else:
            raise TypeError("Function 'ppf' takes 1 to 2 arguments but %d given" % len(args))

    def __str__(self):
        return 'ppf(k=%s)' % self.k

    def geteq(self):
        return sym.Eq(self.k * var.x, var.y)

    def getq(self):
        if self.k > 0:
            return [1, 3]
        elif self.k < 0:
            return [2, 4]

    def getx(self, y):
        return y / self.k

    def gety(self, x):
        return self.k * x

    def plot(self):
        sym.plotting.plot(self.k * var.x)


class qf(object):
    # Quadratic function

    def __init__(self, *args):
        if len(args) == 1:
            if float(args[0]) != 0:
                self.a = args[0]
                self.b = self.c = 0
            else:
                raise TypeError("'a' cannot equals to 0")
        elif len(args) == 2:
            if float(args[0]) != 0:
                self.a = args[0]
                self.b = 0
                self.c = args[1]
            else:
                raise TypeError("'a' cannot equals to 0")
        elif len(args) == 3:
            if float(args[0]) != 0:
                self.a = args[0]
                self.b = args[1]
                self.c = args[2]
            else:
                raise TypeError("'a' cannot equals to 0")
        elif len(args) == 6:
            x1, y1 = args[0], args[1]
            x2, y2 = args[2], args[3]
            x3, y3 = args[4], args[5]
            eq1 = sym.Eq(var.a * x1 ** 2 + var.b * x1 + var.c, y1)
            eq2 = sym.Eq(var.a * x2 ** 2 + var.b * x2 + var.c, y2)
            eq3 = sym.Eq(var.a * x3 ** 2 + var.b * x3 + var.c, y3)
            ans = sym.solve([eq1, eq2, eq3], [var.a, var.b, var.c])
            self.a, self.b, self.c = ans.values()
        else:
            raise TypeError("Function 'qf' takes 1, 2, 3 or 6 arguments but %d given" % len(args))

    def __str__(self):
        return 'qf(a=%s, b=%s, c=%s)' % (self.a, self.b, self.c)

    def geteq(self):
        return sym.Eq(self.a * var.x ** 2 + self.b * var.x + self.c, var.y)

    def getx(self, y):
        delta = self.b ** 2 - 4 * self.a * self.c
        if delta < 0:
            return
        elif delta == 0:
            return -self.b / (2 * self.a)
        else:
            x1 = (-self.b + sym.sqrt(delta)) / (2 * self.a)
            x2 = (-self.b - sym.sqrt(delta)) / (2 * self.a)
            return [x1, x2]

    def gety(self, x):
        return self.a * x ** 2 + self.b * x + self.c

    def plot(self):
        sym.plotting.plot(self.a * var.x ** 2 + self.b * var.x + self.c)


if __name__ == '__main__':
    core().run()
