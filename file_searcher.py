import argparse


class FileSearcher:
    def __init__(self, filepath):
        self.filepath = filepath
        self.history_list = self.get_history_list(self.filepath)

    def get_history_list(self, filepath):
        """ Returns a list of all the previous commands without duplicates """
        history_set = set()  # use set to avoid duplicates
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line[0] != '#':
                    line = line.strip('\n')
                    history_set.add(line)

        history_list = list(history_set)

        return history_list

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
