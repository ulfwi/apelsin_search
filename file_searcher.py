import argparse


class FileSearcher:
    def __init__(self, filepath):
        self.filepath = filepath
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
        self.history_list.remove(phrase)
        with open(self.filepath, 'w') as f:
            f.write('\n'.join(self.history_list) + '\n')

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
