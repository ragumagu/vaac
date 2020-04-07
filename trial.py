'''class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())            
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

getch = _GetchUnix()

ch = getch()
print("ch",ch)
print("type(ch)",type(ch))
print("repr(ch)",repr(ch))
'''

from curses import wrapper

def main(stdscr):
    stdscr.clear()        
    stdscr.addstr("helloworld\n")    
    
    
    stdscr.move(0,3)
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)