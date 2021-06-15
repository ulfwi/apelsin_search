from curses_gui import GUI, exit_curses
from file_searcher import FileSearcher
from utils import Position
from enum import Enum
import traceback


allowed_symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                   'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'å', 'ä', 'ö' 'A', 'B', 'C', 'D',
                   'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                   'Y', 'Z', 'Å', 'Ä', 'Ö', ' ', '/', '\\', '.', '_', '-', '*', '(',
                   ')', '{', '}', '"', '~', '$']

class Mode(Enum):
    none = 0
    typing = 1
    selecting_results = 2

class HistorySearch:
    def __init__(self, bash_history_filepath, bash_history_favorites_filepath):
        self.bash_history_filepath = bash_history_filepath
        self.bash_history_favorites_filepath = bash_history_favorites_filepath
        self.searcher = FileSearcher(self.bash_history_filepath)
        self.favorites_searcher = FileSearcher(self.bash_history_favorites_filepath)
        self.gui = GUI()
        self.mode = Mode.none

        self.pos_search_bar_cursor = Position(0, 0)
        self.pos_search_results = Position(0, 1)

        self.max_nbr_search_results = self.get_max_nbr_search_results()
        self.max_command_length = self.get_max_command_length()

    def get_max_nbr_search_results(self):
        pos_max = self.gui.get_max_pos()
        return pos_max.y - 2

    def get_nbr_search_results(self, nbr_hits):
        return min(self.max_nbr_search_results, nbr_hits)

    def get_max_command_length(self):
        pos_max = self.gui.get_max_pos()
        return pos_max.x - 2

    def extract_result(self, hits, hits_favorites, idx):
        if idx < len(hits_favorites):
            return hits_favorites[idx]
        else:
            return hits[idx - len(hits_favorites)]

    def display_results(self, hits, hits_favorites, result_selection_idx):
        # Clear old results
        self.gui.clear_remainder_of_screen()

        # Print top results
        nbr_hits = len(hits) + len(hits_favorites)
        nbr_search_results = self.get_nbr_search_results(nbr_hits)
        self.gui.goto_pos(self.pos_search_results)
        if hits or hits_favorites:
            for i in range(nbr_search_results):
                command_str = self.extract_result(hits, hits_favorites, i)

                if len(command_str) > self.max_command_length:
                    # Don't print entire command if it's too long
                    command_str = command_str[:self.max_command_length+1]
                else:
                    # Pad with spaces so that selection looks good
                    command_str += " " * (self.max_command_length + 1 - len(command_str))

                if self.mode == Mode.selecting_results and i == result_selection_idx:
                    self.gui.write(command_str + '\n', 2)
                else:
                    self.gui.write(command_str + '\n', 1)

    def handle_special_chars(self, key):
        # TODO Add support for å, ä, ö
        start = 200
        # for i in range(start, start + 50):
        #     self.gui.write(str(i) + ": " + chr(i) + '\n')
        # self.gui.write(str(ord(key)))
        # self.gui.write(str(len(key)))
        if key == '¥':
            key = 'å'
        elif key == '¤':
            key = 'ä'
        # elif ord(key) == 246:
        #     key = 'ö'

        # self.gui.write(str(ord(key)))

        # 214: Ö
        # 196: Ä
        # 197: Å
        # 246: ö

        return key

    def run(self):
        self.mode = Mode.typing
        self.gui.write("$ ")
        self.pos_search_bar_cursor = self.gui.get_cursor_pos()

        search_phrase = ""
        result_selection_idx = 0
        hits = []
        hits_favorites = []
        return_command = True
        while True:
            key = self.gui.get_key()
            key = self.handle_special_chars(key)

            if key == 'KEY_BACKSPACE':
                self.mode = Mode.typing
                self.gui.goto_pos(self.pos_search_bar_cursor)
                if search_phrase:
                    self.gui.remove_last_char()
                    search_phrase = search_phrase[:-1]

                self.pos_search_bar_cursor = self.gui.get_cursor_pos()
            elif (len(key) == 1) and (ord(key) == 24):
                # Ctrl-x
                return_command = False
                break
            elif key == '\n':
                break
            elif key in ['KEY_RIGHT', 'KEY_LEFT']:
                pass
            elif key in ['KEY_UP', 'KEY_DOWN']:
                nbr_hits = len(hits) + len(hits_favorites)
                nbr_search_results = self.get_nbr_search_results(nbr_hits)
                if self.mode != Mode.selecting_results:
                    result_selection_idx = 0
                elif nbr_search_results != 0:
                    if key == 'KEY_DOWN':
                        result_selection_idx = (result_selection_idx + 1) % nbr_search_results
                    else:
                        result_selection_idx = (result_selection_idx - 1) % nbr_search_results
                self.mode = Mode.selecting_results
            elif key == 'KEY_RESIZE':
                # Update max size
                self.max_nbr_search_results = self.get_max_nbr_search_results()
                self.max_command_length = self.get_max_command_length()
            elif key in allowed_symbols:
                if len(search_phrase) < self.max_command_length - 1:
                    self.mode = Mode.typing
                    self.gui.goto_pos(self.pos_search_bar_cursor)
                    search_phrase += key
                    self.gui.write(key)
                    self.pos_search_bar_cursor = self.gui.get_cursor_pos()

            # Update results
            if self.mode == Mode.typing:
                search_phrase_list = search_phrase.split(' ')
                hits = self.searcher.search_for_phrases(search_phrase_list)
                hits_favorites = self.favorites_searcher.search_for_phrases(search_phrase_list)

            self.display_results(hits, hits_favorites, result_selection_idx)

            # Move cursor back
            self.gui.goto_pos(self.pos_search_bar_cursor)

        result = ""
        if return_command and (hits or hits_favorites):
            if self.mode == Mode.selecting_results:
                result = self.extract_result(hits, hits_favorites, result_selection_idx)
            else:
                result = self.extract_result(hits, hits_favorites, 0)

        return result


if __name__ == '__main__':
    apelsin_dir = '/home/s0001191/repos/apelsin_search'
    bash_history_filepath = '/home/s0001191/.bash_history'
    bash_history_favorites_filepath = apelsin_dir + '/.bash_history_favorites'

    try:
        history_search = HistorySearch(bash_history_filepath, bash_history_favorites_filepath)
        output = history_search.run()

        # Write result to file
        with open(apelsin_dir + "/search_result", "w") as f:
            f.write(output)
    except:
        exit_curses()
        traceback.print_exc()
        exit(1)

    exit(0)
