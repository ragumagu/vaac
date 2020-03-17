import csv
from fuzzywuzzy import fuzz
import subprocess

def __docs__():
    '''
    This is the extractor module. When given a string, it will extract the command and application name, and return them as a list.
    It assumes some basic settings:
            Default browser: Mozilla Firefox.
            Text editor: Gedit.
            IDE: Visual Studio Code.
            Terminal: Gnome-terminal.

    Commands can be chained using the word "and".
    "open","focus","switch to" commands are also supported.
    
    '''


class extractor():
    '''This is the extractor class.'''

    def __init__(self):        
        self.applications = [['mozilla-firefox','mozilla','browser','firefox'], ['text-editor','gedit'], ['visual-studio-code','vs-code','code'], ['terminal','gnome-terminal']]
        code_shortcuts_file = open(
            "./data/code_keyboard_shortcuts.csv")  # Hardcoded string
        self.code_keyboard_shortcuts = list(csv.reader(code_shortcuts_file))
        firefox_shortcuts_file = open(
            "./data/firefox_keyboard_shortcuts.csv")  # Hardcoded string
        self.firefox_keyboard_shortcuts = list(
            csv.reader(firefox_shortcuts_file))
        gedit_shortcuts_file = open(
            "./data/gedit_keyboard_shortcuts.csv")  # Hardcoded string
        self.gedit_keyboard_shortcuts = list(csv.reader(gedit_shortcuts_file))
        terminal_shortcuts_file = open(
            "./data/terminal_keyboard_shortcuts.csv")  # Hardcoded string
        self.terminal_keyboard_shortcuts = list(
            csv.reader(terminal_shortcuts_file))

        # vaac_commands_file = open("./data/vaac_commands.csv") #Hardcoded string
        #self.vaac_commands = list(csv.reader(vaac_commands_file))

        self.map = {"code": self.code_keyboard_shortcuts, "firefox": self.firefox_keyboard_shortcuts,
                    "gedit": self.gedit_keyboard_shortcuts, "terminal": self.terminal_keyboard_shortcuts}

        self.current_app = ""


    def find_open_applications(self):
        string = subprocess.getoutput("./vaac_code/running_apps.sh").lower()
        open_applications = string.split("\n")
        
        #print("Executor.find_open_applications():",open_applications)
        return open_applications

    def find_target_application(self,string):
        '''Stores target application in self.current_app and returns the input string after removing the target application from it, for further processing.'''

        new_app = "?"
        for i in range(len(self.applications)):
            for app in self.applications[i]:
                if app in string:
                    new_app = self.applications[i][-1]
                    string = string.replace(app, '').strip()
                    break

        #print("Current target application", self.current_app)
        #print("New target application", new_app)


        if new_app != "?" or self.current_app == "":
            self.current_app = new_app
        #else: ? this should throw an error.
        return string

    def find_command_type(self,string):
        '''Classifies commands into open, type or key types, which will be later used as arguments to xdotool.'''
        if string == "open":
            cmd_type = "open"
        elif string == "type":
            cmd_type = "type"
        else:
            cmd_type = "key"
        return cmd_type        

    def find_commands(self, string):
        commands = string.split("and")
        result = []
        for command in commands:            
            command = command.strip()
            result.append(self.extract(command))
        #print("Extractor.find_commands(): ",commands)
        print("Extractor returning:",result)
        return result

    def extract(self, string):
        print("Extractor.extract():Processing string:",string)
        string = self.find_target_application(string)
        cmd_type = self.find_command_type(string)
        open_applications = self.find_open_applications()
        if cmd_type == "open":            
            if self.current_app in open_applications:
                return ['focus',self.current_app]
            else:
                return ['open',self.current_app]

        if self.current_app not in open_applications:
            print("Extractor: Command not clear! Please try again.")
            return None

        if string == "focus" or string == "switch to":
            return ['focus',self.current_app]
        #if cmd_type == "type":
        #if string == "key":
                    
        max_ratio = 0
        i = 0
        n = 0
        for line in self.map[self.current_app]:
            tsr = fuzz.token_sort_ratio(string, line[0])
            #print("string:",string,"line",line,"tsr",tsr)
            if tsr > max_ratio:
                max_ratio = tsr
                n = i

            i += 1

        print("Extractor: max_ratio:", max_ratio)
        print("Extractor: command is",self.map[self.current_app][n])
        
        if max_ratio > 50:
            command = self.map[self.current_app][n][1:]        
            command.append(self.current_app)
            command.insert(0, cmd_type)
            #print("Extractor, sending command:", command)
            return command
        else:
            print("Extractor: Command not clear! Please try again.")
            return None
