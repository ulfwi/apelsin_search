import traceback

from curses_gui import GUI, exit_curses

CTRL_X = '\x18'
CTRL_F = '\x06'
PRE_UMLAUT = 'Ã'
A_RING = '¥'
O_UMLAUT = '¶'
A_UMLAUT = '¤'
A_RING_CAPITAL = '\x85'
A_UMLAUT_CAPITAL = '\x84'
O_UMLAUT_CAPITAL = '\x96'


def loop():
    gui = GUI()
    gui.write("$ ")

    while True:
        key = gui.get_key()
        if key == PRE_UMLAUT:
            key = gui.get_key()
            if key == A_RING:
                key = 'å'
            elif key == A_UMLAUT:
                key = 'ä'
            elif key == O_UMLAUT:
                key = 'ö'
            elif key == A_RING_CAPITAL:
                key = 'Å'
            elif key == A_UMLAUT_CAPITAL:
                key = 'Ä'
            elif key == O_UMLAUT_CAPITAL:
                key = 'Ö'
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
    except KeyboardInterrupt:
        exit_curses()
    except:
        exit_curses()
        traceback.print_exc()
