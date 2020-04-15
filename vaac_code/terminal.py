'''This is the terminal module for Vaac'''
import curses
import logging
from curses import ascii, wrapper
from vaac_code.extractor import Extractor
from vaac_code.window_manager import WindowManager

class WindowHandler:
    def __init__(self, stdscr, screen_pad, inputHandler, maxlines):
        self.stdscr = stdscr
        self.pad = screen_pad
        self.y_offset = 0
        self.cursor_y = 1
        self.cursor_x = len(inputHandler.prompt)
        self.maxlines = maxlines

    def writeInput(self, inputHandler):
        curses.update_lines_cols()
        self.pad.resize(self.maxlines, curses.COLS)
        self.pad.erase()
        self.pad.addstr(str(inputHandler.commands_list)+'\n')
        self.pad.addstr(inputHandler.screen_log)
        self.pad.addstr(inputHandler.prompt+''.join(inputHandler.command))
    
    def updateyx(self, inputHandler):        
        y, x = self.pad.getyx()
        char = inputHandler.char.value
        
        self.cursor_x = (inputHandler.cmd_char_idx.value +
                         len(inputHandler.prompt)) % curses.COLS
        self.cursor_y = y

        if char == curses.KEY_PPAGE:
            self.y_offset -= curses.LINES - 1
            if self.y_offset < 0:
                self.y_offset = 0
        elif char == curses.KEY_NPAGE:
            self.y_offset += curses.LINES - 1
            if self.y_offset + curses.LINES >= self.cursor_y:
                self.y_offset = y - curses.LINES + 1
        elif y >= curses.LINES-1:
            self.y_offset = y - curses.LINES + 1

        if (self.y_offset == y - curses.LINES + 1) or (self.y_offset == 0 and (inputHandler.screen_log.count("\n") < curses.LINES)):
            curses.curs_set(2)
        else:
            curses.curs_set(0)

    def move_cursor(self):  
        self.pad.move(self.cursor_y, self.cursor_x)

    def refresh(self):
        try:
            self.pad.refresh(self.y_offset, 0, 0, 0, curses.LINES-1, curses.COLS)
        except Exception as ex:
            logging.critical(str(ex))        

class InputHandler:
    def __init__(self, command, cmd_char_idx, char, stdscr, pad):
        # command is a multiprocessing.manager.list proxy object; it is a list 
        # of chars        
        self.command = command
        # command is a multiprocessing.manager.Value(int) proxy object; it is a # pointer to chars in command.
        self.cmd_char_idx = cmd_char_idx
        # command is a multiprocessing.manager.Value(int) proxy object; it holds
        # the input char from getch().
        self.char = char
                
        self.stdscr = stdscr
        self.pad = pad
        
        self.commands_list = []
        self.cmd_list_pointer = len(self.commands_list)
        self.resizeBool = False        
        self.insertMode = False
        self.exitstring = "exit"
        self.prompt = "> "
        self.screen_log = ('This is the vaac terminal program.\n'
                           + 'Type "help" for more information.\n')

        wm = WindowManager()	
        self.extractor = Extractor(wm)

    def takeInput(self, **kwargs):
        if len(kwargs) == 0:
            self.char.value = self.stdscr.getch()
        if len(kwargs) == 1:
            self.char.value = int(kwargs.pop('char'))        

    def processArgs(self):
        self.resizeBool = False

        if self.char.value >= 32 and self.char.value <= 126:
            logging.debug("cmd_char_idx:"+str(self.cmd_char_idx.value))
            logging.debug("len(self.command):"+str(len(self.command)))
            if self.insertMode:
                if self.cmd_char_idx.value < len(self.command):
                    self.command[self.cmd_char_idx.value] = chr(self.char.value)
                else:
                    self.command.append(chr(self.char.value))
            else:
                self.command.insert(self.cmd_char_idx.value, chr(self.char.value))
            self.cmd_char_idx.value += 1
        
        if self.char.value == curses.KEY_IC:
            self.insertMode = not self.insertMode
            
        elif self.char.value == curses.KEY_UP:
            self.cmd_list_pointer -= 1
            if self.cmd_list_pointer < 0:
                self.cmd_list_pointer = 0

            while len(self.command) > 0:
                self.command.pop()

            for ch in self.commands_list[self.cmd_list_pointer]:
                self.command.append(ch)

            self.cmd_char_idx.value = len(self.command)

        elif self.char.value == curses.KEY_DOWN:
            self.cmd_list_pointer += 1
            if self.cmd_list_pointer >= len(self.commands_list):
                self.cmd_list_pointer = len(self.commands_list)-1

            while len(self.command) > 0:
                self.command.pop()

            for ch in self.commands_list[self.cmd_list_pointer]:
                self.command.append(ch)

            self.cmd_char_idx.value = len(self.command)

        elif self.char.value == curses.KEY_BACKSPACE:            
            if len(self.command) != 0:                
                del self.command[self.cmd_char_idx.value-1]
                self.cmd_char_idx.value -= 1
        
        elif self.char.value == curses.KEY_DC:            
            try:
                if self.cmd_char_idx.value < (len(self.command)):
                    del self.command[self.cmd_char_idx.value]
            except IndexError:
                logging.exception("Could not delete.")

        elif self.char.value == ord('\n') and len(self.command) != 0:
            self.cmd_list_pointer += 1

            if len(self.commands_list) != 0 and self.commands_list[-1] == "":
                self.commands_list.pop()

            command_string = "".join(self.command)
            self.commands_list.append(command_string)
            self.getOutput()  # Probable spaghetti
            self.commands_list.append("")

            while len(self.command) > 0:
                self.command.pop()

            self.cmd_char_idx.value = 0

        elif self.char.value == curses.KEY_LEFT:
            if self.cmd_char_idx.value > 0:
                self.cmd_char_idx.value -= 1
            
        elif self.char.value == curses.KEY_RIGHT:
            if self.cmd_char_idx.value < len(self.command):
                self.cmd_char_idx.value += 1
            
        elif self.char.value == curses.KEY_HOME:
            self.cmd_char_idx.value = 0
            
        elif self.char.value == curses.KEY_END:
            self.cmd_char_idx.value = len(self.command)
            
        elif self.char.value == curses.KEY_RESIZE:            
            self.resizeBool = True

    def checkIfExit(self):
        # The index error occurs initially, when no command has been entered.
        try:
            if self.commands_list[-2] == self.exitstring:
                return True
        except IndexError as ie:
            return False

    def getLastInput(self):
        return self.commands_list[-1]

    def getOutput(self):        
        input_command = self.commands_list[-1]
        logging.debug("input: "+input_command)
        self.screen_log += self.prompt+input_command+"\n"        

        if input_command == 'exit':
            return        
        else:            
            output = self.extractor.extract_and_run(input_command)
            if output is not None:
                self.screen_log += output
