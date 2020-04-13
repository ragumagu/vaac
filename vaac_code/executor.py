import subprocess
from subprocess import Popen
'''This is the Executor module.
	Usage:
		This works on Linux systems with X. Requires wmctrl and xdotool to be installed.	
'''


class Executor():
    '''The Executor class provides methods to send events to other applications.'''

    def __init__(self, wm):
        self.wm = wm
        self.executor_script_path = './vaac_code/executor.sh'
        self.open_string = 'open'
        self.focus_string = 'focus'

    def run(self, commands):
        '''This takes in, a list argument with:
                command[0] = 'key' or 'open' or 'focus'
                command[1] = 'key_stroke_string'
                command[2] = 'target_application_name'
            The key_stroke string is not included, when using 'open' or 'focus'.
            Usage examples:
                # Send key stroke to app:
                >>> executor.run(['key','ctrl+a', 'app']) 
                # Open app:
                >>> executor.run(['open','app']) 
                # Focus app window.
                >>> executor.run(['focus','app']) 
        '''

        print("Executor run received", commands)
        for command in commands:
            if command is None:
                return
            elif command[0] == self.open_string:
                pid = Popen(command[1]).pid
                self.wm.resize_window(pid, command[1])
            elif command[0] == self.focus_string:
                self.wm.focus(command[1])
            else:
                c = command[:]
                self.wm.focus(command[2])
                c.insert(0, self.executor_script_path)
                subprocess.run(c)
                self.wm.resize_if_windows_changed()
