from curses import wrapper,ascii
import curses

class WindowHandler():
    def __init__(self,stdscr,logfile):
        self.stdscr = stdscr
        self.logfile = logfile
    def initscreen(self):
        self.stdscr.erase()
        self.stdscr.addstr("[]\n> ")
        self.stdscr.refresh()        
        self.logfile.write("In windowhandler.initscreen():Screen Initialized.\n")

    def writeInput(self,inputDtoObj):
        self.logfile.write("In windowhandler.writeInput()\n")
        self.stdscr.erase()    
        self.stdscr.addstr(str(inputDtoObj.commands_list))
        #for cmd in inputDtoObj.commands_list:
            #self.stdscr.addstr(inputDtoObj.prompt+cmd+"\n")
        self.stdscr.addstr(inputDtoObj.termOutput+"\n")
        if inputDtoObj.buffer ==[]:
            #print the following also, when debugging
            #stdscr.addstr("current_command"+str(cursor)+"> "+current_command)
            self.stdscr.addstr("> "+"".join(inputDtoObj.current_command))
        else:
            #print the following also, when debugging            
            #stdscr.addstr("buffer,"+str(cursor)+"> "+buffer)            
            self.stdscr.addstr("> "+"".join(inputDtoObj.buffer))
    def move_cursor(self,inputDtoObj):
        self.logfile.write("In windowHandler.move_cursor,moving to y,x:"+str(inputDtoObj.y)+","+str(inputDtoObj.x)+"\n")
        self.stdscr.move(inputDtoObj.y,inputDtoObj.x)
    def refresh(self):
        self.stdscr.refresh()
        self.logfile.write("----------------------\n")

class InputDto:
    def __init__(self,stdscr,logfile):
        self.buffer = [] # list of chars
        self.current_command = [] # list of chars
        self.commands_list = []
        self.cursor = len(self.commands_list)
        self.char = ""
        self.exitstring = "exit"
        self.prompt = "> "
        self.y = 1
        self.x = len(self.prompt)        
        self.stdscr = stdscr        
        self.logfile = logfile
        self.updateBool = False
        self.termOutput = ""
    def takeyx(self):
        self.y,self.x = self.stdscr.getyx()
    def takeInput(self):
        self.logfile.write("In InputDto.takeInput(): taking input...\n")
        self.char = self.stdscr.getch()
        self.logfile.write("In  InputDto.takeInput(): got char="+str(self.char)+"\n")
    def processArgs(self):        
        if self.char >= 32 and self.char <= 126:
            self.cursor = len(self.commands_list)
            if self.buffer != []:
                self.current_command += self.buffer 
                self.buffer = []
            self.takeyx() #probable spaghetti
            self.current_command.insert(self.x-len(self.prompt),chr(self.char))
            self.updateBool = True
        elif self.char == curses.KEY_UP and self.cursor > 0:
            self.cursor -=1
            self.buffer = self.commands_list[self.cursor]
        elif self.char == curses.KEY_DOWN:            
            self.cursor += 1
            if self.cursor < len(self.commands_list):
                self.buffer = list(self.commands_list[self.cursor])
            elif self.cursor == len(self.commands_list):
                self.buffer = []
            elif self.cursor > len(self.commands_list):
                self.cursor = len(self.commands_list)
        elif self.char == curses.KEY_BACKSPACE:
            if self.buffer != []:                
                self.current_command = list(self.buffer)[:-1]
                self.logfile.write("In InputDto.processArgs(): Backspace...Copying buffer[:-1] to current_command.\n")
                self.buffer = []                
            elif self.current_command != []:                
                if self.x == len(self.current_command)+len(self.prompt):
                    self.logfile.write("In InputDto.processArgs(): Backspace...pop\n")
                    self.current_command.pop()                    
                elif self.x < len(self.current_command)+len(self.prompt):
                    self.logfile.write("In InputDto.processArgs(): Backspace...removing:"+str(self.current_command[self.x-len(self.prompt)-1])+"\n")
                    del self.current_command[self.x-len(self.prompt)-1]
            self.updateBool = True
        elif self.char == ord('\n') and self.current_command != []:
            self.cursor += 1
            current_command_string = "".join(self.current_command)
            self.commands_list.append(current_command_string)
            self.getOutput() # Probable spaghetti
            self.current_command = []
            self.buffer = []
        elif self.char == ord('\n') and self.buffer != []:
            self.cursor += 1
            current_command_string = "".join(self.buffer)
            self.commands_list.append(current_command_string)            
            self.current_command = []
            self.buffer = []            
        elif self.char == curses.KEY_LEFT:            
            self.updateBool = True
        elif self.char == curses.KEY_RIGHT:            
            self.updateBool = True
        elif self.char == curses.KEY_HOME:
            self.updateBool = True
        elif self.char == curses.KEY_END:
            self.updateBool = True
        else:
            self.updateBool = False
        self.logfile.write("In  InputDto.processArgs: currentcommand "+"".join(self.current_command)+"\n")
        self.logfile.write("In  InputDto.processArgs: buffer: "+str(self.buffer)+"\n")
        self.logfile.write("In  InputDto.processArgs: commands_list: "+str(self.commands_list)+"\n")
        
    def updateyx(self):
        y,x = self.stdscr.getyx()
        if not self.updateBool:
            return
        self.logfile.write("In InputDto.updateyx:Self y,x"+str(self.y)+","+str(self.x)+"\n")
        self.logfile.write("In InputDto.updateyx:New y,x"+str(y)+","+str(x)+"\n")
        if self.char >= 32 and self.char <= 126:
            self.logfile.write("In InputDto.updateyx:Same x,y(autoincrement)"+"\n")
            self.x = self.x +1
            self.y = y
        elif self.char == curses.KEY_UP or self.char == curses.KEY_DOWN:
            if self.buffer != []:
                self.x = len(self.buffer) + len(self.prompt)                
            else:
                self.x = len(self.current_command) + len(self.prompt)
            self.y = y
        elif self.char == curses.KEY_BACKSPACE:            
            #if self.x < len(self.current_command)+len(self.prompt):
            if self.x > len(self.prompt):
                self.logfile.write("In InputDto.updateyx:AutoDecrement x"+"\n")
                self.x = self.x -1
                self.y = y
        elif self.char == curses.KEY_LEFT:
            if self.x > len(self.prompt):
                self.logfile.write("In InputDto.updateyx:Decrement x"+"\n")
                self.x = self.x -1
                self.y = y
        elif self.char == curses.KEY_RIGHT:
            if self.buffer != []:
                if self.x < len(self.buffer) + len(self.prompt):
                    self.logfile.write("In InputDto.updateyx:Increment x"+"\n")
                    self.x = self.x + 1
                    self.y = y
            elif self.x < len(self.current_command) + len(self.prompt):
                self.logfile.write("In InputDto.updateyx:Increment x"+"\n")
                self.x = self.x + 1
                self.y = y
        elif self.char == ord('\n') and self.current_command == []:
            self.x = len(self.prompt)
            self.y = y
        elif self.char == curses.KEY_HOME:
            self.x = len(self.prompt)
        elif self.char == curses.KEY_END:
            if self.buffer != []:
                self.x = len(self.buffer) + len(self.prompt)
            elif self.current_command != []:
                self.x = len(self.current_command) + len(self.prompt)
        self.logfile.write("In InputDto.updateyx:Final y,x"+str(self.y)+","+str(self.x)+"\n")
    
    def checkIfExit(self):
        try:
            if self.commands_list[-1] == self.exitstring:                
                return True
        except:
            return False

    def getOutput(self):
        self.termOutput += "\n"+self.prompt+self.commands_list[-1]+"\n"
        input_command = self.commands_list[-1]
        import subprocess
        self.termOutput += subprocess.getoutput(input_command)
        self.logfile.write("In inputDto.getOutput,termOutput"+self.termOutput+"\n")
    
def main(stdscr):
    logfile = open("log","w",buffering=1)
    inputDto = InputDto(stdscr,logfile)
    windowHandler = WindowHandler(stdscr,logfile)
    windowHandler.initscreen()
    while 1:        
        inputDto.takeInput()
        inputDto.processArgs()        
        windowHandler.writeInput(inputDto)
        inputDto.updateyx()
        windowHandler.move_cursor(inputDto)
        windowHandler.refresh()
        if inputDto.checkIfExit():
            logfile.write("In  main: Exiting"+"\n")
            break
    
wrapper(main)