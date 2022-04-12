import traceback

from curses_gui import exit_curses
from debug import clear_debug_log, debug_print
from history_search_core import HistorySearchCore
from utils import write_to_terminal_input

if __name__ == '__main__':
    apelsin_dir = '/home/s0001191/repos/apelsin_search'
    bash_history_filepath = '/home/s0001191/.bash_history'
    bash_history_favorites_filepath = apelsin_dir + '/.bash_history_favorites'

    # clear_debug_log()

    try:
        history_search = HistorySearchCore(bash_history_filepath, bash_history_favorites_filepath)
        output = history_search.run()
        write_to_terminal_input(output)
    except KeyboardInterrupt:
        exit_curses()
        exit(1)
    except:
        exit_curses()
        traceback.print_exc()
        exit(1)
