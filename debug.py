DEBUG_OUTPUT_FILE = "/home/s0001191/repos/apelsin_search/output.txt"

def clear_debug_log():
    with open(DEBUG_OUTPUT_FILE, "w") as f:
        f.write('')


def debug_print(message):
    if not isinstance(message, str):
        message = str(message)

    with open(DEBUG_OUTPUT_FILE, "a") as f:
        f.write(message + '\n')
