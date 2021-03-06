import curses
from utils import Position
from enum import Enum


def exit_curses():
    curses.echo()
    curses.endwin()

class CursesColors(Enum):
    UbuntuPurple = 0
    Green = 1

COLOR_UBUNTU_PURPLE = 0

class CursesColorPairs(Enum):
    Normal = 0
    Select = 1

# https://docs.python.org/3/howto/curses.html
class GUI:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_color(COLOR_UBUNTU_PURPLE, 4*48, 4*10, 4*36)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.noecho()
        # curses.cbreak()
        self.stdscr.keypad(True)

    def get_key(self):
        return self.stdscr.getkey()

    def get_cursor_pos(self):
        y, x = self.stdscr.getyx()
        return Position(x, y)

    def get_max_pos(self):
        y, x = self.stdscr.getmaxyx()
        return Position(x, y)

    def goto_pos(self, pos):
        self.stdscr.move(pos.y, pos.x)

    def write(self, string, color_pair=1):
        if not isinstance(string, str):
            string = str(string)

        self.stdscr.addstr(string, curses.color_pair(color_pair))

    def write_and_highlight(self, string, words):
        """ Print string and highlight any occurances of words """

        def insert_between(lst, item):
            result = [item] * (len(lst) * 2 - 1)
            result[0::2] = lst
            return result

        string_list = [string]
        for word in words:
            new_string_list = []
            for substring in string_list:
                new_string_list += insert_between(substring.split(word), word)
            string_list = new_string_list

        for substring in string_list:
            if substring in words:
                self.write(substring, color_pair=3)
            else:
                self.write(substring, color_pair=1)

    def remove_last_char(self):
        # Remove last letter
        pos = self.get_cursor_pos()
        new_pos = Position(pos.x-1, pos.y)
        self.goto_pos(new_pos)
        self.write(' ')
        self.goto_pos(new_pos)

    def clear_remainder_of_screen(self):
        self.stdscr.clrtobot()

    def __del__(self):
        # curses.nocbreak()
        self.stdscr.keypad(False)
        exit_curses()
