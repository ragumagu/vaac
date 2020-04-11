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

    def run(self, input_commands_list):
        '''This takes in, a list argument with:
                command[0] = 'key' or 'open' or 'focus'
                command[1] = 'key_stroke_string'
                command[2] = 'target_application_name'
            The key_stroke string is not included, when using 'open' or 'focus'.
            Usage examples:
                >>> executor.run(['key','ctrl+a', 'app']) # To send keys to app.
                >>> executor.run(['open','app']) # Opens app
                >>> executor.run(['focus','app']) # Focus app                
        '''

        print("Executor run received", input_commands_list)
        for command in input_commands_list:
            if command is None:
                return
            elif command[0] == "open":
                pid = Popen(command[1]).pid
                self.wm.resize_window(pid, command[1])
            elif command[0] == "focus":
                self.wm.focus(command[1])
            else:
                c = command[:]
                self.wm.focus(command[2])
                c.insert(0, self.executor_script_path)
                subprocess.run(c)
                self.wm.resize_if_windows_changed()
