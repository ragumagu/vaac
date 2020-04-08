from curses import wrapper
import curses

def main(stdscr):
  pad = curses.newpad(10+1, 10+1)
  # These loops fill the pad with letters; addch() is
  # explained in the next section
  for y in range(0, 10):
      for x in range(0, 10):
          pad.addch(y, x, ord('a')+y+x)

  # Displays a section of the pad in the middle of the screen.
  # (0,0) : coordinate of upper-left corner of pad area to display.
  # (5,5) : coordinate of upper-left corner of window area to be filled
  #         with pad content.
  # (20, 75) : coordinate of lower-right corner of window area to be
  #          : filled with pad content.
  pad.refresh(1, 0, 0, 0, 8,9)
  pad.getkey()
  '''
    import curses
    pad = curses.newpad(200, curses.COLS)
    pad.keypad(False)
    filelength = 0

    linesnum = 0
    logfile = open("triallog", "w", buffering=1)
    with open("log", "r") as inputfile:
        for line in inputfile:
            for char in line:
                pad.addch(char)
            filelength += len(line)
            logfile.write(repr(line)+"\n")
            rem = len(line)
            while rem> 0:
              linesnum += 1
              rem = curses.COLS % rem

    endx = 0
    endy = linesnum
    # linesnum = filelength // curses.COLS
    logfile.write("Filelenght:"+str(filelength)+"\n")
    logfile.write("linesnum:"+str(linesnum)+"\n")
    logfile.write("cols:"+str(curses.COLS)+"\n")
    logfile.write("lines:"+str(curses.LINES)+"\n")
    cursor = 0
    char = 0
    pad.refresh(cursor, 0, 0, 0, curses.LINES-1, curses.COLS)

    while(1):
        char = pad.getch()
        # stdchar = stdscr.getch()
        logfile.write("got char "+str(char)+"\n")
        # logfile.write("got stdchar "+str(stdchar)+"\n")
        if char == ord('q'):
            break
        elif char == ord('j'):
            if cursor < linesnum:
                cursor += 1
            if cursor >= linesnum:
                cursor = linesnum - 1
        elif char == ord('k'):
            if cursor > 0:
                cursor -= 1
        elif char == 27:
            lst = [27]
            for i in range(3):
                lst.append(pad.getch())
            logfile.write("Got 27\n")
            logfile.write("lst= "+str(lst)+"\n")
            if lst == [27, 91, 53, 126]:
                logfile.write("Got pageup\n")
                cursor -= curses.LINES - 1
                if cursor < 0:
                    cursor = 0
            elif lst == [27, 91, 54, 126]:
                logfile.write("Got pagedown\n")
                cursor += curses.LINES - 1
                if cursor >= linesnum:
                    cursor = linesnum - 1
        elif char >= 32 and char <= 126:
            logfile.write("Got printable char.\n")
            pad.addch(char)
            cursor = linesnum + 1
            endx += 1
            pad.move(cursor, endx)
            pad.refresh(cursor, 0, 0, 0, curses.LINES-1, curses.COLS)
            continue
        elif char == ord('\n'):
            pad.addch(char)
            linesnum += 1
            cursor = linesnum
            endx = 0
            pad.move(cursor, 0)
            pad.refresh(cursor, 0, 0, 0, curses.LINES-1, curses.COLS)
            continue

        pad.move(cursor, 0)
        pad.refresh(cursor, 0, 0, 0, curses.LINES-1, curses.COLS)

'''
wrapper(main)
