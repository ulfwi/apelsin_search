
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def write_to_terminal_input(cmd):
    import fcntl
    import termios
    for c in cmd:
        fcntl.ioctl(0, termios.TIOCSTI, c)
