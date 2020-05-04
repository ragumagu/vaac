'''This is the window manager module for vaac.'''
import ast
import logging
import subprocess
from collections import defaultdict


class WindowManager():
    def __init__(self):
        # window_pointers keeps pointers to window ids
        self.window_pointers = dict()
        self.update_apps_windows()

    def get_active_window_class(self):
        # wmctrl : lists open windows
        # $(xdotool getwindowfocuse getwindowname) : title of current window
        # grep : gets first title name match from wmctrl output
        # cut : extracts the window class name from grep output
        # tr : converts output to lower case
        cmd = 'wmctrl -lx | grep -m1 "$(xdotool getwindowfocus getwindowname)" | cut -d" " -f4 | cut -d"." -f2 | tr "[:upper:]" "[:lower:]"'
        output = subprocess.getoutput(cmd)
        return output

    def update_apps_windows(self):
        command = "./vaac_code/running_apps.sh"
        output_string = subprocess.getoutput(command).lower()
        try:
            output = ast.literal_eval(output_string)
        except Exception:
            logging.warn("Got an invalid string.")
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
        '''Call this method to cycle between windows of the same app. You have
        to call focus after calling this method to focus the next window.'''
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
            logging.warning(target_app + " is not open to be focused.")

    def get_open_apps(self):
        return self.apps_windows_dict.keys()
