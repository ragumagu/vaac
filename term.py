from curses import wrapper,ascii
import curses

class WindowHandler():
    def __init__(self,stdscr,screen_pad,logfile):        
        self.stdscr = stdscr
        self.pad = screen_pad
        self.logfile = logfile
    def initscreen(self):
        self.stdscr.refresh()
        self.pad.erase()
        self.pad.addstr("[]\n> ")
        self.pad.refresh(0, 0, 0, 0, curses.LINES-1, curses.COLS)
        self.logfile.write("In windowhandler.initscreen():Screen Initialized:"+str(curses.LINES)+","+str(curses.COLS)+"\n")

    def writeInput(self,inputDtoObj):
        self.logfile.write("In windowhandler.writeInput()\n")
        self.pad.erase()    
        self.pad.addstr(str(inputDtoObj.commands_list)+"\n")
        self.pad.addstr(inputDtoObj.screen_log)
        self.pad.addstr("> "+"".join(inputDtoObj.command))
        
    def move_cursor(self,inputDtoObj):
        self.logfile.write("In windowHandler.move_cursor,moving to y,x:"+str(inputDtoObj.cursor_y)+","+str(inputDtoObj.cursor_x)+"\n")
        self.pad.move(inputDtoObj.cursor_y,inputDtoObj.cursor_x)
    def refresh(self,inputDtoObj):
        self.pad.refresh(inputDtoObj.y_offset,0, 0, 0, curses.LINES-1, curses.COLS)
        self.logfile.write("----------------------\n")

class InputHandler:
    def __init__(self,stdscr,screen_pad,logfile):
        self.screen_log = "" # list of chars
        self.command = [] # list of chars
        self.commands_list = []        
        self.char = 0
        self.exitstring = "exit"
        self.prompt = "> "
        self.cursor_y = 1
        self.cursor_x = len(self.prompt)
        self.y_offset = 0
        self.cmd_list_pointer = 0
        self.cmd_char_idx = 0
        self.stdscr = stdscr
        self.pad = screen_pad
        self.logfile = logfile
        self.updateBool = False        
    def takeyx(self):
        self.cursor_y,self.cursor_x = self.pad.getyx()
    def takeInput(self):        
        self.char = self.stdscr.getch()
        self.logfile.write("In  InputDto.takeInput(): Got char:"+str(self.char)+"\n")
    def processArgs(self):        
        if self.char >= 32 and self.char <= 126:
            self.takeyx() #probable spaghetti
            self.command.insert(self.cmd_char_idx,chr(self.char))
            self.cmd_char_idx += 1
            #self.command.insert(self.cursor_x-len(self.prompt),chr(self.char))
            self.updateBool = True

        elif self.char == curses.KEY_UP:
            self.cmd_list_pointer -= 1
            if  self.cmd_list_pointer < 0:
                self.cmd_list_pointer = 0
            self.command = list(self.commands_list[self.cmd_list_pointer])
            self.cmd_char_idx = len(self.command)
        elif self.char == curses.KEY_DOWN:            
            self.cmd_list_pointer += 1
            if self.cmd_list_pointer >= len(self.commands_list):
                self.cmd_list_pointer = len(self.commands_list)-1
            self.command = list(self.commands_list[self.cmd_list_pointer])
            self.cmd_char_idx = len(self.command)
            
        elif self.char == curses.KEY_BACKSPACE:                         
            if self.command != []:
                self.logfile.write("In InputDto.processArgs(): Backspace...removing:"+str(self.command[self.cursor_x-len(self.prompt)-1])+"\n")
                del self.command[self.cursor_x-len(self.prompt)-1]
                self.cmd_char_idx -= 1
            self.updateBool = True
        elif self.char == ord('\n') and self.command != []:
            self.cmd_list_pointer += 1            
            if self.commands_list != [] and self.commands_list[-1] == "":
                self.commands_list.pop() # Careful!

            command_string = "".join(self.command)
            self.commands_list.append(command_string)
            self.getOutput() # Probable spaghetti
            self.commands_list.append("")
            while len(self.command) > 0:
                self.command.pop()
            self.cmd_char_idx = 0        
        
        elif self.char == curses.KEY_LEFT:           
            if self.cmd_char_idx > 0:
                self.cmd_char_idx -= 1
            self.updateBool = True
        elif self.char == curses.KEY_RIGHT:            
            if self.cmd_char_idx < len(self.command):
                self.cmd_char_idx += 1
            self.updateBool = True
        elif self.char == curses.KEY_HOME:
            self.cmd_char_idx = 0
            self.updateBool = True
        elif self.char == curses.KEY_END:
            self.cmd_char_idx = len(self.command)
            self.updateBool = True
        elif self.char == curses.KEY_NPAGE:                        
            self.updateBool = True
        elif self.char == curses.KEY_PPAGE:
            self.updateBool = True
        else:
            self.updateBool = False
        self.logfile.write("In  InputDto.processArgs: currentcommand "+"".join(self.command)+"\n")        
        self.logfile.write("In  InputDto.processArgs: commands_list: "+str(self.commands_list)+"\n")
        self.logfile.write("In  InputDto.processArgs: cmd_char_idx: "+str(self.cmd_char_idx)+"\n")
    def updateyx(self):
        y,x = self.pad.getyx()
        if not self.updateBool:
            return
        self.logfile.write("In InputDto.updateyx:Self y,x"+str(self.cursor_y)+","+str(self.cursor_x)+"\n")
        self.logfile.write("In InputDto.updateyx:New y,x"+str(y)+","+str(x)+"\n")
        self.cursor_x = (self.cmd_char_idx+len(self.prompt))%curses.COLS
        self.cursor_y = y
        
        if self.char == curses.KEY_PPAGE:
            self.logfile.write("Got pageup\n")            
            self.y_offset -= curses.LINES - 1
            if self.y_offset < 0:
                self.y_offset = 0            
        elif self.char == curses.KEY_NPAGE:
            self.logfile.write("Got pagedown\n")
            self.y_offset += curses.LINES - 1
            if self.y_offset + curses.LINES >= self.cursor_y:
                self.y_offset = y - curses.LINES + 1            
        elif y >= curses.LINES-1:
            self.y_offset = y - curses.LINES + 1
        if self.y_offset == y - curses.LINES + 1:
            curses.curs_set(2)
        else:
            curses.curs_set(0)
    
    def checkIfExit(self):
        try:
            if self.commands_list[-2] == self.exitstring:                
                return True
        except:
            return False

    def getOutput(self):
        self.screen_log += self.prompt+self.commands_list[-1]+"\n"        
        input_command = self.commands_list[-1]
        import subprocess
        self.screen_log += subprocess.getoutput(input_command)+"\n"
        #self.logfile.write("In inputDto.getOutput,"+self.termOutput+"\n")
        
def main(stdscr):
    logfile = open("log","w",buffering=1)
    pad = curses.newpad(200, curses.COLS) #Change this to maxlinesize.
    inputHandler = InputHandler(stdscr,pad,logfile)
    windowHandler = WindowHandler(stdscr,pad,logfile)
    windowHandler.initscreen()
    while 1:        
        inputHandler.takeInput()
        inputHandler.processArgs()        
        windowHandler.writeInput(inputHandler)
        inputHandler.updateyx()
        windowHandler.move_cursor(inputHandler)
        windowHandler.refresh(inputHandler)
        if inputHandler.checkIfExit():
            logfile.write("In  main: Exiting..."+"\n")
            logfile.close()
            break
    
wrapper(main)