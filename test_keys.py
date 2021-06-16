from curses_gui import GUI, exit_curses
import traceback

CTRL_X = '\x18'
CTRL_F = '\x06'

def loop():
    gui = GUI()
    gui.write("$ ")

    while True:
        key = gui.get_key()
        # if (len(key) == 1) and (ord(key) == 24):
        if key == CTRL_X:
            break
        elif key == CTRL_F:
            gui.write("Favorite")
        elif key == 'KEY_DC':
            pass
        elif key == '\n':
            break
        else:
            gui.write(key)
            if len(key) == 1:
                gui.write(ord(key))


if __name__ == '__main__':

    try:
        loop()
    except:
        exit_curses()
        traceback.print_exc()
        exit(1)

    exit(0)