'''This is the window manager module for vaac.'''
from collections import defaultdict
import ast
import subprocess
import logging
class WindowManager():
    def __init__(self):
        # window_pointers keeps pointers to window ids
        self.window_pointers = dict()  
        self.update_apps_windows()        

    def update_apps_windows(self):
        logging.info("WindowManager:Updating wm values.")
        command = "./vaac_code/running_apps.sh"
        output_string = subprocess.getoutput(command).lower()        
        try:
            output = ast.literal_eval(output_string)
        except:
            logging.warn("update_apps_windows: Got an invalid string.")
            return
        apps_windows_dict = defaultdict(list)
        for item in output:
            apps_windows_dict[item['key']].append(item['value'])
        self.apps_windows_dict = apps_windows_dict
        self.update_window_pointers()  # Possible spaghetti

    def update_window_pointers(self):
        A = set(self.apps_windows_dict.keys())
        B = set(self.window_pointers.keys())
        add = A.difference(B)
        remove = B.difference(A)
        for item in add:
            self.window_pointers[item] = 0
        for item in remove:
            del self.window_pointers[item]
        
    def cycle_index(self, app):
        '''Call this method to cycle between windows of the same app. You have to call focus after calling this method to focus the next window.'''
        self.window_pointers[app] += 1
        if self.window_pointers[app] == len(self.apps_windows_dict[app]):
            self.window_pointers[app] = 0
       
    def focus(self, target_app):        
        if target_app in self.apps_windows_dict:
            pointer = self.window_pointers[target_app]
            target_win_id = str(self.apps_windows_dict[target_app][pointer])
            command = ['xdotool', 'windowactivate', target_win_id]
            subprocess.run(command)            
        else:
            print("WindowManager:", target_app, "is not open to be focused.")
    
    def get_open_apps(self):
        return self.apps_windows_dict.keys()