import os


def remove_cmd_from_bash_history(cmd_to_remove, bash_history_filename):
    line_to_remove = cmd_to_remove + '\n'
    tmp_filename = '.bash_history_tmp'

    with open(bash_history_filename, 'r') as f_in, open(tmp_filename, 'w') as f_out:
        # Every second line in bash history is a timestamp and should start with hashtag
        is_timestamp_line = True
        is_first_line_in_file = True

        timestamp_line = ""
        for line in f_in:
            if is_first_line_in_file:
                # Check if first line in file is timestamp or not
                is_timestamp_line = (line[0] == '#')

            if is_timestamp_line:
                if line[0] != '#':
                    os.remove(tmp_filename)
                    raise Exception("Expected line starting with hashtag. Instead got: " + line)
                is_timestamp_line = False
                timestamp_line = line
            else:
                if line_to_remove == line:
                    # Remove command
                    is_timestamp_line = True
                else:
                    if not is_first_line_in_file:
                        f_out.write(timestamp_line)
                    f_out.write(line)
                    is_timestamp_line = True

            is_first_line_in_file = False

    # Replace with new bash history file and add _old suffix to the old bash history file
    os.rename(bash_history_filename, bash_history_filename + '_old')
    os.rename(tmp_filename, bash_history_filename)


class FileSearcher:
    def __init__(self, filepath, has_timestamps=False):
        self.filepath = filepath
        self.has_timestamps = has_timestamps
        self.history_list = self.read_history_list_from_file(self.filepath)

    def read_history_list_from_file(self, filepath):
        """ Returns a list of all the previous commands without duplicates """
        history_list = []
        with open(filepath, 'r') as f:
            for line in f:
                if line[0] != '#':
                    line = line.strip('\n')
                    if line not in history_list:
                        history_list.append(line)

        return history_list

    def get_history_list(self):
        return self.history_list

    def remove_phrase_in_file(self, phrase):
        phrase_removed = False
        if phrase in self.history_list:
            self.history_list.remove(phrase)

            if self.has_timestamps:
                remove_cmd_from_bash_history(phrase, self.filepath)
            else:
                with open(self.filepath, 'w') as f:
                    f.write('\n'.join(self.history_list) + '\n')

            phrase_removed = True

        return phrase_removed

    def add_phrase_to_file(self, phrase):
        self.history_list.append(phrase)
        with open(self.filepath, 'a') as f:
            f.write(phrase + '\n')

    def search_for_phrases(self, phrases):
        """ Returns a list of commands from history_list that contains all phrases """
        hits = []
        for line in self.history_list:
            # Only return line if it contains all phrases
            contains_all_phrases = all(
                (phrase in line) for phrase in phrases)

            if contains_all_phrases:
                hits.append(line)

        return hits


if __name__ == '__main__':
    import argparse
    description = r"""Search in command history.
    Bjorn Ulfwi, 2021.
    """
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('phrases', nargs='*', type=str, help='Phrases to search for.')
    args = parser.parse_args()

    filepath = '/home/s0001191/.bash_history'
    phrases = args.phrases
    # phrases = ['qac', 'validator']

    print('Searching for phrases: ' + str(phrases))

    searcher = FileSearcher(filepath)
    hits = searcher.search_for_phrases(phrases)

    print('\nHits: ')
    for hit in hits:
        print(hit)
