import curses
from utils import Position


# https://docs.python.org/3/howto/curses.html
class GUI:
    def __init__(self):
        self.stdscr = curses.initscr()
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

    def write(self, string):
        self.stdscr.addstr(string)

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
        curses.echo()
        curses.endwin()