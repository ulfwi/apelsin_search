import fcntl
import termios


def write_to_terminal_input(cmd):
    for c in cmd:
        fcntl.ioctl(0, termios.TIOCSTI, c)
