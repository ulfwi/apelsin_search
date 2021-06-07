import curses
from history import Searcher


filepath = '/home/s0001191/.bash_history'

searcher = Searcher(filepath)

# https://docs.python.org/3/howto/curses.html

stdscr = curses.initscr()
curses.noecho()
# curses.cbreak()
stdscr.keypad(True)

stdscr.addstr("$ ")
search_phrase = ""
while True:
    key = stdscr.getkey()
    y_search_bar_cursor, x_search_bar_cursor = stdscr.getyx()
    if key == 'KEY_BACKSPACE':
        if search_phrase:
            # Remove last letter
            stdscr.move(y_search_bar_cursor, x_search_bar_cursor-1)
            y_search_bar_cursor, x_search_bar_cursor = stdscr.getyx()
            stdscr.addstr(' ')
            stdscr.move(y_search_bar_cursor, x_search_bar_cursor)
            search_phrase = search_phrase[:-1]
    elif key == '\n':
        break
    elif key in ['KEY_RIGHT', 'KEY_LEFT', 'KEY_UP', 'KEY_DOWN']:
        pass
    else:
        search_phrase += key
        stdscr.addstr(key)

    y_search_bar_cursor, x_search_bar_cursor = stdscr.getyx()

    hits = searcher.search_for_phrases(search_phrase.split(' '))
    y_max, x_max = stdscr.getmaxyx()

    nbr_search_results = max(y_max - 5, 5)
    y_search_results = y_search_bar_cursor + 1

    # Clear old results
    stdscr.clrtobot()

    # Print top results
    stdscr.move(y_search_results, 0)
    if hits:
        for i in range(min(nbr_search_results, len(hits) - 1)):
            try:
                command_str = hits[i]
                if len(command_str) >= x_max-1:
                    # Don't print entire command if it's too long
                    command_str = command_str[:x_max-1]
                stdscr.addstr(command_str + '\n')
            except:
                break

    # Move cursor back
    stdscr.move(y_search_bar_cursor, x_search_bar_cursor)


# Exit
# curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

print(search_phrase)
