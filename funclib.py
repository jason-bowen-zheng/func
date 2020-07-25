# func/funclib.py
# func runtime lib

import sys

class core(object):

    def __init__(self):
        self.function = {}

    def run(self):
        while True:
            try:
                cmd = input('> ')
            except KeyboardInterrupt:
                print()
                sys.exit(1)
            else:
                pass
