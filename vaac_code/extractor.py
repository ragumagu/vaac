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

class Extractor():
    '''This is the extractor class.'''

    def __init__(self,wm):
        self.wm = wm
        self.applications = [['mozilla-firefox', 'mozilla', 'browser', 'firefox'], ['text-editor', 'gedit'], [
            'visual-studio-code', 'vs-code', 'code'], ['terminal', 'gnome-terminal'], ['files', 'nautilus']]
        self.app_names = ['code','firefox','gedit','general','nautilus','gnome-terminal']
        paths = ["./data/keys/code_keyboard_shortcuts.csv","./data/keys/firefox_keyboard_shortcuts.csv","./data/keys/gedit_keyboard_shortcuts.csv","./data/keys/general_keyboard_shortcuts.csv","./data/keys/nautilus_keyboard_shortcuts.csv","./data/keys/terminal_keyboard_shortcuts.csv"]
        self.files_map = {}        
        for i in range(len(paths)):
            dfile = open(paths[i],"r")
            self.files_map[self.app_names[i]] = list(csv.reader(dfile))        
        self.current_app = ""

    def find_target_application(self, string):
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
        # else: ? this should throw an error.
        return string

    def find_command_type(self, string):
        '''Classifies commands into open, type or key types, which will be later used as arguments to xdotool.'''
        if string == "open":
            cmd_type = "open"
        elif string == "type":
            cmd_type = "type"
        else:
            cmd_type = "key"
        return cmd_type

    def find_commands(self, string):
        string = string.lower()
        commands = string.split("and")
        result = []
        for command in commands:
            command = command.strip()
            result.append(self.extract(command))        
        return result

    def extract(self, string):
        #print("Extractor.extract():Processing string:", string)
        string = self.find_target_application(string)
        cmd_type = self.find_command_type(string)        
        self.wm.update_apps_windows()
        self.wm.window_dims = self.wm.get_window_dims_dict()
        print("wm.window_dims_dict",self.wm.window_dims) # Remove this
        open_applications = self.wm.get_open_apps()
        if cmd_type == "open":
            if self.current_app in open_applications:
                return ['focus', self.current_app]
            else:
                return ['open', self.current_app]

        if self.current_app not in open_applications:
            print("Extractor: Command not clear! Please try again.")
            return None

        if string == "focus" or string == "switch to":
            return ['focus', self.current_app]
        # if cmd_type == "type":
        # if string == "key":

        max_ratio = 0
        i = 0
        n = 0
        for line in self.files_map[self.current_app]:
            tsr = fuzz.token_sort_ratio(string, line[0])
            # print("string:",string,"line",line,"tsr",tsr)
            if tsr > max_ratio:
                max_ratio = tsr
                n = i

            i += 1

        print("Extractor: max_ratio:", max_ratio)
        print("Extractor: command is", self.files_map[self.current_app][n])

        if max_ratio == 100:
            command = self.files_map[self.current_app][n][1:]
            command.append(self.current_app)
            command.insert(0, cmd_type)
            #print("Extractor, sending command:", command)
            return command
        else:
            print("Extractor: Command not clear! Please try again.")
            return None
