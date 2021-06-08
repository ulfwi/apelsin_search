from curses_gui import GUI
from file_searcher import FileSearcher
from utils import Position


class HistorySearch:
    def __init__(self, filepath):
        self.filepath = filepath
        self.searcher = FileSearcher(self.filepath)
        self.gui = GUI()

    def run(self):
        self.gui.write("$ ")
        search_phrase = ""
        while True:
            key = self.gui.get_key()
            if key == 'KEY_BACKSPACE':
                if search_phrase:
                    self.gui.remove_last_char()
                    search_phrase = search_phrase[:-1]
            elif key == '\n':
                break
            elif key in ['KEY_RIGHT', 'KEY_LEFT', 'KEY_UP', 'KEY_DOWN']:
                pass
            else:
                search_phrase += key
                self.gui.write(key)

            pos_search_bar_cursor = self.gui.get_cursor_pos()

            search_phrase_list = search_phrase.split(' ')
            hits = self.searcher.search_for_phrases(search_phrase_list)
            pos_max = self.gui.get_max_pos()

            max_nbr_search_results = max(pos_max.y - 5, 5)
            pos_search_results = Position(0, pos_search_bar_cursor.y + 1)

            # Clear old results
            self.gui.clear_remainder_of_screen()

            # Print top results
            self.gui.goto_pos(pos_search_results)
            if hits:
                nbr_search_results = min(max_nbr_search_results, len(hits))
                for i in range(nbr_search_results):
                    try:
                        command_str = hits[i]
                        if len(command_str) >= pos_max.x-1:
                            # Don't print entire command if it's too long
                            command_str = command_str[:pos_max.x-1]
                        self.gui.write(command_str + '\n')
                    except:
                        break

            # Move cursor back
            self.gui.goto_pos(pos_search_bar_cursor)

        return search_phrase


if __name__ == '__main__':
    filepath = '/home/s0001191/.bash_history'
    history_search = HistorySearch(filepath)
    output = history_search.run()

    del history_search

    print(output)

