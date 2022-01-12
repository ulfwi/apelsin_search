import fcntl
import termios
import traceback
from enum import Enum

from curses_gui import GUI, exit_curses
from file_searcher import FileSearcher
from utils import Position

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
        self.nbr_displayed_search_results = 0

    def get_max_nbr_search_results(self):
        pos_max = self.gui.get_max_pos()
        return pos_max.y - 2

    def get_max_command_length(self):
        pos_max = self.gui.get_max_pos()
        return pos_max.x - 2

    def display_results(self, hits, result_selection_idx, search_phrase_list):
        # Clear old results
        self.gui.clear_remainder_of_screen()

        # Print top results
        self.nbr_displayed_search_results = min(self.max_nbr_search_results, len(hits))
        self.gui.goto_pos(self.pos_search_results)
        if hits:
            for i in range(self.nbr_displayed_search_results):
                command_str = hits[i]

                if len(command_str) > self.max_command_length:
                    # Don't print entire command if it's too long
                    command_str = command_str[:self.max_command_length+1]
                else:
                    # Pad with spaces so that selection looks good
                    command_str += " " * (self.max_command_length + 1 - len(command_str))

                if self.mode == Mode.selecting_results and i == result_selection_idx:
                    self.gui.write(command_str + '\n', 2)
                elif search_phrase_list and search_phrase_list[0] != '':
                    self.gui.write_and_highlight(command_str + '\n', search_phrase_list)
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
        hits = self.favorites_searcher.get_history_list() + self.searcher.get_history_list()
        search_phrase_list = []
        execute_cmd = False
        entry_deleted = False
        while True:
            # Display results
            self.display_results(hits, result_selection_idx, search_phrase_list)

            # Move cursor back
            self.gui.goto_pos(self.pos_search_bar_cursor)

            # Handle input keys
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
                raise KeyboardInterrupt
            elif key == '\n':
                execute_cmd = True
                break
            elif key == 'KEY_RIGHT':
                execute_cmd = False
                break
            elif key in ['KEY_UP', 'KEY_DOWN']:
                if self.mode != Mode.selecting_results:
                    if key == 'KEY_DOWN':
                        result_selection_idx = 0
                    elif key == 'KEY_UP':
                        result_selection_idx = self.nbr_displayed_search_results - 1
                elif self.nbr_displayed_search_results != 0:
                    if key == 'KEY_DOWN':
                        result_selection_idx = (result_selection_idx + 1) % self.nbr_displayed_search_results
                    elif key == 'KEY_UP':
                        result_selection_idx = (result_selection_idx - 1) % self.nbr_displayed_search_results
                self.mode = Mode.selecting_results
            elif key == 'KEY_RESIZE':
                # Update max size
                self.max_nbr_search_results = self.get_max_nbr_search_results()
                self.max_command_length = self.get_max_command_length()
                if result_selection_idx > self.max_nbr_search_results:
                    result_selection_idx = 0
            elif key == 'KEY_DC':
                if self.mode == Mode.selecting_results:
                    selected_phrase = hits[result_selection_idx]
                    self.favorites_searcher.remove_phrase_in_file(selected_phrase)
                    entry_deleted = True
            elif key in allowed_symbols:
                if len(search_phrase) < self.max_command_length - 1:
                    self.mode = Mode.typing
                    self.gui.goto_pos(self.pos_search_bar_cursor)
                    search_phrase += key
                    self.gui.write(key)
                    self.pos_search_bar_cursor = self.gui.get_cursor_pos()

            if self.mode == Mode.typing or entry_deleted:
                # Update results
                entry_deleted = False
                search_phrase_list = search_phrase.split(' ')
                search_phrase_list = [phrase for phrase in search_phrase_list if phrase != '']
                hits = self.favorites_searcher.search_for_phrases(search_phrase_list) \
                    + self.searcher.search_for_phrases(search_phrase_list)

        result = ""
        if hits:
            if self.mode == Mode.selecting_results:
                result = hits[result_selection_idx]
            else:
                result = hits[0]

            if execute_cmd:
                result += '\n'

        return result


def writeToTerminalInput(cmd):
    for c in cmd:
        fcntl.ioctl(0, termios.TIOCSTI, c)


if __name__ == '__main__':
    apelsin_dir = '/home/s0001191/repos/apelsin_search'
    bash_history_filepath = '/home/s0001191/.bash_history'
    bash_history_favorites_filepath = apelsin_dir + '/.bash_history_favorites'

    try:
        history_search = HistorySearch(bash_history_filepath, bash_history_favorites_filepath)
        output = history_search.run()
        writeToTerminalInput(output)
    except KeyboardInterrupt:
        exit_curses()
        exit(1)
    except:
        exit_curses()
        traceback.print_exc()
        exit(1)
