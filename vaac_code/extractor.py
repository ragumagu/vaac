'''The extractor module assumes some defaults:
            Browser: Mozilla Firefox.
            Text editor: Gedit.
            IDE: Visual Studio Code.
            Terminal: Gnome-terminal.
            Files: Nautilus.    
    'open','focus','switch to', 'go to' commands are also supported.
'''

import csv
import logging
from fuzzywuzzy import fuzz

import vaac_code.executor as executor


class Extractor:
    '''Extractor class provides methods to extract commands and run them.
    The filter_* methods set self.found to True if a matching command is 
    found, or False otherwise. Filter methods return the matched command.
    '''

    def __init__(self, wm):
        self.wm = wm
        self.current_app = wm.get_active_window_class()
        self.target_app = ''
        self.command = ''
        self.applications = [
            ['visual studio code', 'vs code', 'code'],
            ['mozilla firefox', 'mozilla', 'browser', 'firefox'],
            ['text editor', 'gedit'],
            ['files', 'nautilus'],
            ['terminal', 'gnome-terminal'],
        ]
        self.app_names = [
            'code', 'firefox', 'gedit',
            'general', 'nautilus', 'gnome-terminal',
        ]
        self.files_map = {}
        for app_name in self.app_names:
            path = f'./data/keys/{app_name}_keyboard_shortcuts.csv'
            with open(path, 'r') as dfile:  # data file
                self.files_map[app_name] = list(csv.reader(dfile))

    def extract_and_run(self, command):
        self.command = command
        cmd = self.extract()
        
        if isinstance(cmd, list):
            executor.run(cmd, self.wm)
            return None
        else:
            return cmd

    def filter_help(self):
        if self.command == 'help':
            if self.target_app == '?':
                self.found = True
                with open('./vaac_code/vaac_terminal_help.txt', 'r') as helptxt:
                    return helptxt.read()
            else:
                self.found = True
                lst = [str(item[0]).lower()
                    for item in self.files_map[self.target_app]]
                return '\n'.join(lst)+'\n'
        else:
            self.found = False
            return None

    def filter_open(self):
        if self.command == 'open':
            if self.target_app == '?':
                self.found = False
                return None
            elif self.target_app in self.open_applications:
                self.found = True
                self.current_app = self.target_app
                return ['focus', self.target_app]
            else:
                self.found = True
                self.current_app = self.target_app
                return ['open', self.current_app]
        else:
            self.found = False
            return None

    def filter_focus(self):
        if self.command in ['focus', 'go to', 'switch to', ''] and self.target_app != '?':
            self.found = True
            self.current_app = self.target_app
            return ['focus', self.current_app]
        else:
            self.found = False
            return None

    def filter_match(self):
        if self.target_app != '?':
            self.current_app = self.target_app
        matched_command = max(self.files_map[self.current_app],
                              key=lambda x: fuzz.token_sort_ratio(self.command, x[0]))

        max_ratio = fuzz.token_sort_ratio(self.command, matched_command[0])

        logging.debug('max_ratio: '+str(max_ratio))
        logging.debug('target_app is '+self.current_app)
        logging.debug('command is '+str(matched_command))

        if max_ratio == 100:            
            result = matched_command[1:]            
            result.append(self.current_app)
            result.insert(0, 'key')
            self.found = True
            return result
        else:
            self.found = False
            return None

    def extract(self):
        '''Matches self.command with various filters, and returns resulting command as a list.'''
        self.command = self.command.lower().strip()
        self.find_target_application()
        
        self.wm.update_apps_windows()
        self.open_applications = self.wm.get_open_apps()

        filters = [
            self.filter_help,
            self.filter_open,
            self.filter_focus,
            self.filter_match,
        ]

        result = None
        self.found = False

        for filter in filters:
            result = filter()
            if self.found:
                break

        if result is None:
            logging.warning('Extractor: Command not clear! Please try again.')
        return result

    def find_target_application(self):
        self.target_app = '?'
        for applist in self.applications:
            for app in applist:
                if app in self.command:
                    self.target_app = applist[-1]
                    self.command = self.command.replace(app, '').strip()
                    break
