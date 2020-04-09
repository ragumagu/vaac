import curses
from curses import wrapper

def main(stdscr):
    inp = 48
    y,x = stdscr.getmaxyx()
    stdscr.clear()
    #stdscr.nodelay(1)
    pad = curses.newpad(200, curses.COLS)
    logfile = open("log","w",buffering=1)
    logfile.write("Before while loop:lines"+str(curses.LINES)+" cols: "+str(curses.COLS)+"\n")
    while inp != 27:
        while True:
            pad.erase()
            pad.addstr(y-1,0, 'got '+str(inp))
            try:                
                pad.refresh(0,0,0,0,y-1,curses.COLS)    
            except curses.error:                
                curses.update_lines_cols()
                y,x = stdscr.getmaxyx()
                pad = curses.newpad(200, curses.COLS)
                pass
                            
            inp = stdscr.getch()
            if inp == 27:
                break            
            y,x = stdscr.getmaxyx()
            logfile.write("In try:lines "+str(curses.LINES)+" cols: "+str(curses.COLS)+"\n")
            logfile.write("In try:y "+str(y)+" x: "+str(x)+"\n")
    logfile.close()
wrapper(main)