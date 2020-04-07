from curses import wrapper,ascii
import curses

def printstring(stdscr,commands_list,string):
    stdscr.clear()    
    stdscr.addstr(str(commands_list)+"\n")
    stdscr.addstr(string)    
    stdscr.refresh()

def printcurrentcommand(stdscr,commands_list,cursor,buffer,current_command):
    if cursor == len(commands_list):
        #print the following also, when debugging            
        #stdscr.addstr("current_command"+str(cursor)+"> "+current_command)
        stdscr.addstr("> "+"".join(current_command))
    else:
        #print the following also, when debugging            
        #stdscr.addstr("buffer,"+str(cursor)+"> "+buffer)            
        stdscr.addstr("> "+buffer)       

def main(stdscr):
    buffer = ""
    commands_list = []
    cursor = len(commands_list)
    current_command = []
    history = ""
    char = ""
    stdscr.clear()
    stdscr.addstr("> ")
    stdscr.refresh()
    y = 0
    x = 0
    char = ""
    logfile = open("log","w",buffering=1)
    while 1:
        char = stdscr.getch()        
        if char >= 32 and char <= 126:
            cursor = len(commands_list)
            if buffer != "":
                current_command += list(buffer)
            buffer = ""            
            y,x = stdscr.getyx()
            current_command.insert(x-2,chr(char))            
            #y,x = stdscr.getyx()          
            printstring(stdscr,commands_list,history)
            printcurrentcommand(stdscr,commands_list,cursor,buffer,current_command)
            prev_x = x
            y,x = stdscr.getyx()                 
            stdscr.move(y,prev_x+1)
            stdscr.refresh()
            continue

        elif char == curses.KEY_UP and cursor > 0:
            cursor -=1
            buffer = commands_list[cursor]

        elif char == curses.KEY_DOWN:            
            cursor += 1
            if cursor < len(commands_list):
                buffer = commands_list[cursor]
            elif cursor == len(commands_list):
                buffer = ""
            elif cursor > len(commands_list):
                cursor = len(commands_list)

        elif char == curses.KEY_BACKSPACE:
            if buffer != "":
                current_command = list(buffer)[:-1]
                buffer = ""
            elif current_command != []:
                y,x = stdscr.getyx()
                logfile.write("current_command"+str(current_command)+"\n")
                logfile.write("y,x:"+str(y)+","+str(x)+"\n")
                try:
                    if x == len(current_command)+2:
                        logfile.write("popping last character\n")
                        current_command.pop()
                        
                    elif x < len(current_command)+2:
                        logfile.write("deleting at "+str(int(x)-3)+"\n")
                        del current_command[x-3]
                        y,x = stdscr.getyx()    
                        if x > 2:
                            x -= 1  
                        printstring(stdscr,commands_list,history)
                        printcurrentcommand(stdscr,commands_list,cursor,buffer,current_command)
                        stdscr.move(y,x)    
                        stdscr.refresh()
                        continue     
                except IndexError as ie:       
                        logfile.write(str(ie)+"\n")
                        logfile.write("current_command"+str(current_command)+"\n")
                        logfile.write("y,x:"+str(y)+","+str(x)+"\n")
                        logfile.close()
                        break                    

        elif char == ord('\n') and current_command != []:
            cursor += 1
            current_command_string = "".join(current_command)
            commands_list.append(current_command_string)
            history += "> " + current_command_string +"\n"
            current_command = []
            buffer = ""
        elif char == curses.KEY_LEFT:
            y,x = stdscr.getyx()            
            if x > 2:
                x -= 1  
            printstring(stdscr,commands_list,history)
            printcurrentcommand(stdscr,commands_list,cursor,buffer,current_command)
            stdscr.move(y,x)    
            stdscr.refresh()
            continue     
        elif char == curses.KEY_RIGHT:
            y,x = stdscr.getyx()            
            if x <= len(current_command):
                x += 1
            printstring(stdscr,commands_list,history)
            printcurrentcommand(stdscr,commands_list,cursor,buffer,current_command)
            stdscr.move(y,x)            
            stdscr.refresh()
            continue
        
        try:
            if commands_list[-1] == "exit":
                break
        except:
            pass

        printstring(stdscr,commands_list,history)
        printcurrentcommand(stdscr,commands_list,cursor,buffer,current_command)
        stdscr.refresh()
        
    #stdscr.getkey()

wrapper(main)