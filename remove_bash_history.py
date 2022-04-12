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
                    print('Command removed: ' + cmd_to_remove)
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

if __name__ == '__main__':
    # bash_history_filename = '/home/s0001191/.bash_history'
    bash_history_filename = '/home/s0001191/repos/apelsin_search/.bash_history_test'

    # cmd_to_remove = 'git review -R'
    cmd_to_remove = '#1649685282'

    remove_cmd_from_bash_history(cmd_to_remove, bash_history_filename)
