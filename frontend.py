import curses
from history import Searcher

# https://docs.python.org/3/howto/curses.html

class GUI:
    def __init__(self, filepath):
        self.filepath = filepath
        self.searcher = Searcher(self.filepath)

        self.stdscr = curses.initscr()
        curses.noecho()
        # curses.cbreak()
        self.stdscr.keypad(True)

    def run(self):
        self.stdscr.addstr("$ ")
        search_phrase = ""
        while True:
            key = self.stdscr.getkey()
            y_search_bar_cursor, x_search_bar_cursor = self.stdscr.getyx()
            if key == 'KEY_BACKSPACE':
                if search_phrase:
                    # Remove last letter
                    self.stdscr.move(y_search_bar_cursor, x_search_bar_cursor-1)
                    y_search_bar_cursor, x_search_bar_cursor = self.stdscr.getyx()
                    self.stdscr.addstr(' ')
                    self.stdscr.move(y_search_bar_cursor, x_search_bar_cursor)
                    search_phrase = search_phrase[:-1]
            elif key == '\n':
                break
            elif key in ['KEY_RIGHT', 'KEY_LEFT', 'KEY_UP', 'KEY_DOWN']:
                pass
            else:
                search_phrase += key
                self.stdscr.addstr(key)

            y_search_bar_cursor, x_search_bar_cursor = self.stdscr.getyx()

            hits = self.searcher.search_for_phrases(search_phrase.split(' '))
            y_max, x_max = self.stdscr.getmaxyx()

            nbr_search_results = max(y_max - 5, 5)
            y_search_results = y_search_bar_cursor + 1

            # Clear old results
            self.stdscr.clrtobot()

            # Print top results
            self.stdscr.move(y_search_results, 0)
            if hits:
                for i in range(min(nbr_search_results, len(hits) - 1)):
                    try:
                        command_str = hits[i]
                        if len(command_str) >= x_max-1:
                            # Don't print entire command if it's too long
                            command_str = command_str[:x_max-1]
                        self.stdscr.addstr(command_str + '\n')
                    except:
                        break

            # Move cursor back
            self.stdscr.move(y_search_bar_cursor, x_search_bar_cursor)

        return search_phrase

    def __del__(self):
        # Exit
        # curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()


if __name__ == '__main__':
    filepath = '/home/s0001191/.bash_history'
    gui = GUI(filepath)
    output = gui.run()

    del gui

    print(output)

