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
    Filter methods return the matched command.
    '''

    def __init__(self, wm):
        self.wm = wm
        self.current_app = wm.get_active_window_class()
        self.target_app = ''
        self.command = ''
        self.extracted_commands = []
        self.buffer = []
        self.applications = [
            ['visual studio code', 'vs code', 'code'],
            ['mozilla firefox', 'mozilla', 'browser', 'firefox'],
            ['text editor', 'gedit'],
            ['general'],
            ['terminal', 'gnome-terminal'],
            ['files', 'nautilus'],            
        ]
        self.app_names = [
            'code', 'firefox', 'gedit',
            'general', 'gnome-terminal', 'nautilus', 
            'keys',
        ]
        self.files_map = {}
        for app_name in self.app_names:
            path = f'./data/keys/{app_name}.csv'
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

    def filter_repeat(self):
        if (self.command == 'repeat'
            and self.extracted_commands != []):
            result = self.extracted_commands[-1]
            if ((len(result) == 3 and result[2] in self.open_applications)
                or (len(result) == 2)
                or (isinstance(result,str))):
                return result
        return None

    def filter_open(self):
        if self.command == 'help':
            return self.get_help_string(self.target_app)
        elif (self.command in ['open', 'focus', 'go to', 'switch to', '']
              and self.target_app != '?'):
            self.current_app = self.target_app
            if self.target_app in self.open_applications:
                return ['focus', self.target_app]
            else:
                return ['open', self.current_app]
        elif (self.command in ['focus next','focus other window','focus next window']):
            self.wm.cycle_index(self.current_app)
            return ['focus', self.current_app]
        else:
            return None

    def get_help_string(self, app_name):
        if app_name == '?':
            with open('./vaac_code/vaac_terminal_help.txt', 'r') as helptxt:
                return helptxt.read()
        else:
            with open(f'./config/{app_name}.csv', 'r') as helptxt:
                lst = [item[0] for item in csv.reader(helptxt)]
                return '\n'.join(lst)+'\n'

    def filter_search(self):
        if self.target_app != '?':
            self.current_app = self.target_app
        targets = [self.current_app,'general','keys']
        for target in targets:
            matched_command = self.match(target)
            if matched_command is not None:
                break
        return matched_command

    def match(self,app_name):
        matched_command = max(self.files_map[app_name],
                              key=lambda x: fuzz.token_sort_ratio(self.command, x[0]))

        max_ratio = fuzz.token_sort_ratio(self.command, matched_command[0])
        if max_ratio == 100:
            result = matched_command[1:]
            if app_name not in ['general',]:
                result.append(self.current_app)
            result.insert(0, 'key')
            return result
        else:
            return None

    def clear_buffer(self):
        logging.debug('clearing buffer')
        for i in range(len(self.buffer)):
            self.buffer.pop()

    def filter_buffer(self):
        '''Runs all filters on self.buffer if no match is found in other.'''
        self.buffer.append(self.command)        
        self.command = ' '.join(self.buffer)
        logging.debug('command in buffer is '+self.command)
        
        filters = [
            self.filter_repeat, self.filter_open, self.filter_search,
        ]
        
        result = None
        for filter in filters:
            result = filter()
            if result is not None:
                break
                
        return result

    def extract(self):
        '''Matches self.command with various filters, and returns resulting command as a list.'''
        self.command = self.command.lower().strip()
        self.find_target_application()

        self.wm.update_apps_windows()
        self.open_applications = self.wm.get_open_apps()

        filters = [
            self.filter_repeat, self.filter_open, self.filter_search,
            self.filter_buffer,
        ]
        result = None
        for filter in filters:
            result = filter()
            if result is not None:
                break

        if result is not None:
            self.clear_buffer()
            self.extracted_commands.append(result) # save result            
        else:
            logging.warning('Command not clear!')
        logging.debug('extractor returning'+str(result))
        return result

    def find_target_application(self):
        self.target_app = '?'
        for applist in self.applications:
            for app in applist:
                if app in self.command:
                    self.target_app = applist[-1]
                    self.command = self.command.replace(app, '').strip()
                    break
