from random import choice
from hex import *
import sys, tty, termios
import curses

UP = chr(65)
DOWN = chr(66)
RIGHT = chr(67)
LEFT = chr(68)

#  3x4
#   __
#  /  \
#  \__/
#
#      __
#   __/  \__
#  /  \__/  \
#  \__/  \__/
#     \__/
#
#

class DumpGenerator:
    def __init__(self, config):
        self.config = config
        self.mapping = {
                'R': Biome.ROAD,
                'L': Biome.LAND,
                'W': Biome.WATER,
                'V': Biome.VILLAGE
        }

    def start(self):
        for conf in self.config:
            yield Hex(*[self.mapping[ch] for ch in conf])
        while True:
            yield Hex(*[self.mapping[choice('RLWV')] for i in range(6)])

class Game:
    def __init__(self, sc):
        # self.log = open('log.log', 'w')

        self.sc = sc
        self.screen_size = sc.getmaxyx()
        self.viewport_size = (self.screen_size[0]-2, self.screen_size[1]-2)
        self.viewport_offset = (0, 0)

        self.sc.keypad(True)

        self.cursor = (0,0)

        self.gen = DumpGenerator([
            'VLLRLL',
            'RLLRRL',
            'RLLVLL',
            'LRLVLL',
            ])

        self.map = Map(self.gen)

    def start(self):
        while True:
            self.render()
            # self.sc.timeout(100)
            self.process_input()
            # delay
    def process_input(self):
        inp_ch = self.sc.getch()
        if 'q' == inp_ch:
            sys.exit(0)
        self.process_move(inp_ch)


    def render(self):
        self.sc.clear()
        for point, hx in self.map.hxs.items():
            pass

        # self.sc.addch('x')

        self.sc.refresh()

    def process_move(self, side):
        if side == curses.KEY_UP:
            self.cursor = dec_y_pair(self.cursor)
        elif side == curses.KEY_DOWN:
            self.cursor = inc_y_pair(self.cursor)
        elif side == curses.KEY_RIGHT:
            self.cursor = inc_x_pair(self.cursor)
        elif side == curses.KEY_LEFT:
            self.cursor = dec_x_pair(self.cursor)

        if self.cursor[0] > self.viewport_size[0]:
            self.viewport_offset = inc_y_pair(self.viewport_offset)
            self.cursor = set_y_pair(self.cursor, self.viewport_size[0])

        if self.cursor[0] < 0:
            self.viewport_offset = dec_y_pair(self.viewport_offset)
            self.cursor = set_y_pair(self.cursor, 0)

        if self.cursor[1] > self.viewport_size[1]:
            self.viewport_offset = inc_x_pair(self.viewport_offset)
            self.cursor = set_x_pair(self.cursor, self.viewport_size[1])

        if self.cursor[1] < 0:
            self.viewport_offset = dec_x_pair(self.viewport_offset)
            self.cursor = set_x_pair(self.cursor, 0)
        self.sc.move(self.cursor[0], self.cursor[1])

def set_x_pair(pair, x):
    return (pair[0], x)

def set_y_pair(pair, y):
    return (y, pair[1])

def inc_y_pair(pair):
    return (pair[0]+1, pair[1])

def dec_y_pair(pair):
    return (pair[0]-1, pair[1])

def inc_x_pair(pair):
    return (pair[0], pair[1]+1)

def dec_x_pair(pair):
    return (pair[0], pair[1]-1)

def main(sc):
    # curses.curs_set(False) # disable blinking cursor
    curses.noecho()
    curses.cbreak()

    g = Game(sc)
    g.start()


if __name__ == "__main__":
    curses.wrapper(main)

