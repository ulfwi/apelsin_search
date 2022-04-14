import argparse
import traceback

from curses_gui import exit_curses
from debug import clear_debug_log, debug_print
from history_search_core import HistorySearchCore
from utils import write_to_terminal_input

if __name__ == '__main__':
    description = r"""Search in command history.
    Bjorn Ulfwi, 2022.
    """
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--bash_history', type=str, help='Path to .bash_history.')
    parser.add_argument('--bash_history_favorites', type=str, help='Path to .bash_history_favorites.')
    args = parser.parse_args()

    # clear_debug_log()

    try:
        history_search = HistorySearchCore(args.bash_history, args.bash_history_favorites)
        output = history_search.run()
        write_to_terminal_input(output)
    except KeyboardInterrupt:
        exit_curses()
        exit(1)
    except:
        exit_curses()
        traceback.print_exc()
        exit(1)
