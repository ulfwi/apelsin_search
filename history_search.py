from curses_gui import GUI
from file_searcher import FileSearcher
from utils import Position
from enum import Enum


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

        self.pos_search_results = Position(0, 1)

    def display_results(self, hits, result_selection_idx):
        pos_max = self.gui.get_max_pos()
        max_nbr_search_results = max(pos_max.y - 5, 5)

        # Clear old results
        self.gui.clear_remainder_of_screen()

        # Print top results
        self.gui.goto_pos(self.pos_search_results)
        if hits:
            nbr_search_results = min(max_nbr_search_results, len(hits))
            for i in range(nbr_search_results):
                try:
                    command_str = hits[i]
                    if len(command_str) >= pos_max.x-1:
                        # Don't print entire command if it's too long
                        command_str = command_str[:pos_max.x-1]

                    if self.mode == Mode.selecting_results and i == result_selection_idx:
                        self.gui.write(command_str + '\n', 2)
                    else:
                        self.gui.write(command_str + '\n', 1)
                except:
                    break

    def update_results(self, search_phrase, result_selection_idx):
        pos_search_bar_cursor = self.gui.get_cursor_pos()

        search_phrase_list = search_phrase.split(' ')
        hits = self.searcher.search_for_phrases(search_phrase_list)

        self.display_results(hits, result_selection_idx)

        # Move cursor back
        self.gui.goto_pos(pos_search_bar_cursor)

        return hits

    def run(self):
        self.mode = Mode.typing
        self.gui.write("$ ")
        search_phrase = ""
        result_selection_idx = 0
        hits = []
        while True:
            key = self.gui.get_key()
            if key == 'KEY_BACKSPACE':
                self.mode = Mode.typing
                if search_phrase:
                    self.gui.remove_last_char()
                    search_phrase = search_phrase[:-1]

            elif key == '\n':
                break
            elif key in ['KEY_RIGHT', 'KEY_LEFT']:
                pass
            elif key in ['KEY_UP', 'KEY_DOWN']:
                if self.mode == Mode.typing:
                    result_selection_idx = 0
                    self.mode = Mode.selecting_results
                elif key == 'KEY_DOWN':
                    # TODO: handle when hits is longer than max_nbr_search_results
                    result_selection_idx = (result_selection_idx + 1) % len(hits)
                else:
                    result_selection_idx = (result_selection_idx - 1) % len(hits)
            elif key == 'KEY_RESIZE':
                pass
            elif key in ['KEY_PPAGE', 'KEY_NPAGE', 'KEY_DC', 'KEY_END', 'KEY_HOME', 'KEY_IC']:
                # Ignore keys
                pass
            else:
                self.mode = Mode.typing
                search_phrase += key
                self.gui.write(key)

            hits = self.update_results(search_phrase, result_selection_idx)

        return hits[result_selection_idx]


if __name__ == '__main__':
    filepath = '/home/s0001191/.bash_history'
    history_search = HistorySearch(filepath)
    output = history_search.run()

    del history_search

    # Write result to file
    with open("search_result", "w") as f:
        f.write(output)

