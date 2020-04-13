'''This is the terminal module for Vaac'''
from curses import wrapper, ascii
import curses
import logging

class WindowHandler():
    def __init__(self, stdscr, screen_pad, inputHandler, maxlines):
        self.stdscr = stdscr
        self.pad = screen_pad
        self.y_offset = 0
        self.cursor_y = 1
        self.cursor_x = len(inputHandler.prompt)
        self.maxlines = maxlines

    def initscreen(self, inputHandler):
        self.stdscr.refresh()
        self.pad.erase()
        self.pad.addstr('[]'+"\n"+inputHandler.screen_log.value+inputHandler.prompt+" ")
        self.pad.refresh(0, 0, 0, 0, curses.LINES-1, curses.COLS)
        logging.info("windowhandler.initscreen():Screen Initialized:" +
                     str(curses.LINES)+","+str(curses.COLS))

    def writeInput(self, inputHandler):
        logging.info("windowhandler.writeInput(): Writing input.")
        if inputHandler.resizeBool:
            logging.debug("windowhandler.writeInput(): Resizing pad.")
            curses.update_lines_cols()
            self.pad.resize(self.maxlines, curses.COLS)

        self.pad.erase()
        self.pad.addstr(str(inputHandler.commands_list)+"\n")
        self.pad.addstr(inputHandler.screen_log.value)
        self.pad.addstr(inputHandler.prompt+"".join(inputHandler.command))
        logging.debug("windowhandler.writeInput():screen_log.value:"+inputHandler.screen_log.value)

    def move_cursor(self, inputHandler):
        logging.debug("windowHandler.move_cursor,moving to y,x:" +
                      str(self.cursor_y)+","+str(self.cursor_x))
        self.pad.move(self.cursor_y, self.cursor_x)

    def refresh(self):
        logging.info("windowHandler.refresh():Refreshing...")
        self.pad.refresh(self.y_offset, 0, 0, 0, curses.LINES-1, curses.COLS)
        logging.info("----------------------")

    def updateyx(self, inputHandler):
        logging.info("windowHandler.updateyx(): Updating y,x.")
        y, x = self.pad.getyx()
        char = inputHandler.char
        if (not inputHandler.updateBool):
            return

        self.cursor_x = (inputHandler.cmd_char_idx.value +
                         len(inputHandler.prompt)) % curses.COLS
        self.cursor_y = y

        if char == curses.KEY_PPAGE:
            logging.debug("Got pageup.")
            self.y_offset -= curses.LINES - 1
            if self.y_offset < 0:
                self.y_offset = 0
        elif char == curses.KEY_NPAGE:
            logging.debug("Got pagedown.")
            self.y_offset += curses.LINES - 1
            if self.y_offset + curses.LINES >= self.cursor_y:
                self.y_offset = y - curses.LINES + 1
        elif y >= curses.LINES-1:
            self.y_offset = y - curses.LINES + 1

        if (self.y_offset == y - curses.LINES + 1) or (self.y_offset == 0 and (inputHandler.screen_log.value.count("\n") < curses.LINES)):
            curses.curs_set(2)
        else:
            curses.curs_set(0)

        logging.debug("windowHandler.updateyx:current y,x" +
                      str(self.cursor_y)+","+str(self.cursor_x))
        logging.debug("windowHandler.updateyx:New y,x"+str(y)+","+str(x))
        logging.debug("windowHandler.updateyx:Lines,cols " +
                      str(curses.LINES)+","+str(curses.COLS))
        logging.debug("windowHandler.updateyx:y-offset " +
                      str(self.y_offset))


class InputHandler():
    def __init__(self, stdscr, screen_pad, input_command_chars, command_length,cmd_char_idx,updateBool,screen_log):
        self.screen_log = screen_log
        self.screen_log.value = '''This is the vaac terminal program.\nType "help" for more information.\n'''
        self.stdscr = stdscr
        self.pad = screen_pad
        self.command = input_command_chars  # list of chars; list proxy object.
        self.command_length = command_length
        self.cmd_char_idx = cmd_char_idx
        self.updateBool = updateBool

        self.resizeBool = False
        self.process = None
        self.commands_list = []
        self.cmd_list_pointer = 0
        self.char = 0
        self.exitstring = "exit"
        self.prompt = "> "


    def takeInput(self):
        self.char = self.stdscr.getch()
        logging.debug("inputHandler.takeInput(): Got char:" +
                      str(self.char))

    def isUpdated(self):
        logging.debug("inputHandler.isUpdated(): self.command:" +
                      str(self.command))
        if self.command_length.value != len(self.command) or self.updateBool:
            self.command_length.value = len(self.command)            
            self.updateBool = True
            logging.debug("inputHandler.isUpdated(): returning True")
            return True
        logging.debug("inputHandler.isUpdated(): returning False")
        return False

    def processArgs(self):
        self.resizeBool = False
        
        if self.char >= 32 and self.char <= 126:
            self.command.insert(self.cmd_char_idx.value, chr(self.char))
            self.cmd_char_idx.value += 1
            self.updateBool = True
        
        elif self.char == curses.KEY_UP:
            self.cmd_list_pointer -= 1
            if self.cmd_list_pointer < 0:
                self.cmd_list_pointer = 0
                
            while len(self.command) > 0:
                self.command.pop()

            for ch in self.commands_list[self.cmd_list_pointer]:
                self.command.append(ch)
            
            self.cmd_char_idx.value = len(self.command)
        
        elif self.char == curses.KEY_DOWN:
            self.cmd_list_pointer += 1
            if self.cmd_list_pointer >= len(self.commands_list):
                self.cmd_list_pointer = len(self.commands_list)-1

            while len(self.command) > 0:
                self.command.pop()

            for ch in self.commands_list[self.cmd_list_pointer]:
                self.command.append(ch)

            self.cmd_char_idx.value = len(self.command)
        
        elif self.char == curses.KEY_BACKSPACE:
            logging.debug("inputHandler.processArgs(): self.command:"+str(self.command))
            if len(self.command) != 0:
                logging.debug("inputHandler.processArgs(): Backspace...removing:" + str(self.command[self.cmd_char_idx.value-1]))
                del self.command[self.cmd_char_idx.value-1]
                self.cmd_char_idx.value -= 1
            self.updateBool = True
        
        elif self.char == ord('\n') and self.command != []:
            self.cmd_list_pointer += 1

            if self.commands_list != [] and self.commands_list[-1] == "":
                self.commands_list.pop()

            command_string = "".join(self.command)
            self.commands_list.append(command_string)
            self.getOutput()  # Probable spaghetti
            self.commands_list.append("")

            while len(self.command) > 0:
                self.command.pop()

            self.cmd_char_idx.value = 0

        elif self.char == curses.KEY_LEFT:
            if self.cmd_char_idx.value > 0:
                self.cmd_char_idx.value -= 1
            self.updateBool = True
        
        elif self.char == curses.KEY_RIGHT:
            if self.cmd_char_idx.value < len(self.command):
                self.cmd_char_idx.value += 1
            self.updateBool = True
        
        elif self.char == curses.KEY_HOME:
            self.cmd_char_idx.value = 0
            self.updateBool = True
        
        elif self.char == curses.KEY_END:
            self.cmd_char_idx.value = len(self.command)
            self.updateBool = True
        
        elif self.char == curses.KEY_NPAGE:
            self.updateBool = True
        
        elif self.char == curses.KEY_PPAGE:
            self.updateBool = True
        
        elif self.char == curses.KEY_RESIZE:
            self.updateBool = True
            self.resizeBool = True
        
        else:
            self.updateBool = False
        
        logging.debug("inputHandler.processArgs: currentcommand " +
                      repr("".join(self.command)))
        logging.debug("inputHandler.processArgs: commands_list: " +
                      str(self.commands_list))
        logging.debug("inputHandler.processArgs: cmd_char_idx.value: " +
                      str(self.cmd_char_idx.value))

    def checkIfExit(self):
        try:
            if self.commands_list[-2] == self.exitstring:
                return True
        except:
            return False

    def getLastInput(self):
        return self.commands_list[-1]

    def getOutput(self):
        self.screen_log.value += self.prompt+self.commands_list[-1]+"\n"
        input_command = self.commands_list[-1].split()
        if input_command == ['exit']:
            return
        
        if input_command == ['help']:
            help_str = '''This is the Vaac terminal. It provides an interface to communicate with your system. You can type into this terminal, or speak into it.\nThis is a primitive terminal and might not support all key strokes.\nThis terminal accepts simple, natural language commands. You can use up and down to navigate through commands history, and page up and page down to scroll. Use backspace to delete a typed character.\nFor help setting up Vaac, use the README.md file, or go to the Vaac github page.\n'''
            self.screen_log.value += help_str