from curses_gui import GUI, exit_curses
from file_searcher import FileSearcher
from utils import Position
from enum import Enum
import traceback


allowed_symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                   'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                   'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                   'Y', 'Z', ' ', '/', '\\', '.', '_', '-', '*', '(',
                   ')', '{', '}', '"', '~', '$']

class Mode(Enum):
    none = 0
    typing = 1
    selecting_results = 2

class HistorySearch:
    def __init__(self, filepath):
        self.filepath = filepath
        self.searcher = FileSearcher(self.filepath)
        self.gui = GUI()
        self.mode = Mode.none

        self.pos_search_bar_cursor = Position(0, 0)
        self.pos_search_results = Position(0, 1)

    def get_nbr_search_results(self, hits):
        pos_max = self.gui.get_max_pos()
        max_nbr_search_results =  max(pos_max.y - 5, 5)
        return min(max_nbr_search_results, len(hits))

    def get_max_command_length(self):
        pos_max = self.gui.get_max_pos()
        return pos_max.x - 2

    def display_results(self, hits, result_selection_idx):
        # Clear old results
        self.gui.clear_remainder_of_screen()

        # Print top results
        nbr_search_results = self.get_nbr_search_results(hits)
        max_command_length = self.get_max_command_length()
        self.gui.goto_pos(self.pos_search_results)
        if hits:
            for i in range(nbr_search_results):
                command_str = hits[i]
                if len(command_str) > max_command_length:
                    # Don't print entire command if it's too long
                    command_str = command_str[:max_command_length+1]

                if self.mode == Mode.selecting_results and i == result_selection_idx:
                    self.gui.write(command_str + '\n', 2)
                else:
                    self.gui.write(command_str + '\n', 1)

    def run(self):
        self.mode = Mode.typing
        self.gui.write("$ ")
        self.pos_search_bar_cursor = self.gui.get_cursor_pos()

        search_phrase = ""
        result_selection_idx = 0
        hits = []
        while True:
            key = self.gui.get_key()
            if key == 'KEY_BACKSPACE':
                self.mode = Mode.typing
                self.gui.goto_pos(self.pos_search_bar_cursor)
                if search_phrase:
                    self.gui.remove_last_char()
                    search_phrase = search_phrase[:-1]

                self.pos_search_bar_cursor = self.gui.get_cursor_pos()

            elif key == '\n':
                break
            elif key in ['KEY_RIGHT', 'KEY_LEFT']:
                pass
            elif key in ['KEY_UP', 'KEY_DOWN']:
                nbr_search_results = self.get_nbr_search_results(hits)
                if self.mode != Mode.selecting_results:
                    result_selection_idx = 0
                elif nbr_search_results != 0:
                    if key == 'KEY_DOWN':
                        result_selection_idx = (result_selection_idx + 1) % nbr_search_results
                    else:
                        result_selection_idx = (result_selection_idx - 1) % nbr_search_results
                self.mode = Mode.selecting_results
            elif key == 'KEY_RESIZE':
                pass
            elif key in allowed_symbols:
                self.mode = Mode.typing
                self.gui.goto_pos(self.pos_search_bar_cursor)
                search_phrase += key
                self.gui.write(key)
                self.pos_search_bar_cursor = self.gui.get_cursor_pos()
            else:
                # elif key in ['KEY_PPAGE', 'KEY_NPAGE', 'KEY_DC', 'KEY_END', 'KEY_HOME', 'KEY_IC']
                # Ignore keys
                pass

            # Update results
            if self.mode == Mode.typing:
                search_phrase_list = search_phrase.split(' ')
                hits = self.searcher.search_for_phrases(search_phrase_list)

            self.display_results(hits, result_selection_idx)

            # Move cursor back
            self.gui.goto_pos(self.pos_search_bar_cursor)

        return hits[result_selection_idx]


if __name__ == '__main__':
    filepath = '/home/s0001191/.bash_history'
    apelsin_dir = '/home/s0001191/repos/history'

    try:
        history_search = HistorySearch(filepath)
        output = history_search.run()

        # Write result to file
        with open(apelsin_dir + "/search_result", "w") as f:
            f.write(output)
    except:
        exit_curses()
        traceback.print_exc()
        exit(1)

    exit(0)
