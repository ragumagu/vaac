import subprocess
from subprocess import Popen
import platform
import time
'''This is the Executor module.
	Usage:
		This works on Linux systems with X. Requires wmctrl and xdotool to be installed.
	TODO:
		# Add support for Windows.
'''

class executor():
    '''This is the Executor class.'''    
    def __init__(self):
        self.platform = platform.system()

    def run(self,input_commands_list):
        '''This takes in, a list argument with:
                command[0] = 'key' or 'type' or 'open' or 'focus'
                command[1] = 'key_stroke_string'
                command[2] = 'target_application_name'
            The key_stroke string is not included, when using 'open'.
            The target application name is optional: if not provided, the key_stroke is sent to the current window.
            Usage examples:
                >>> executor.run(['key','ctrl+a', 'app']) # To send keys to app.
                >>> executor.run(['key','F11']) # Sends key F11 to current window.
                >>> executor.run(['type','this is my name','editor']) # To type into a text editor.
                >>> executor.run(['open','app']) # Opens app
                
        '''
        print("Executor run received",input_commands_list)
        if self.platform == 'Linux':
            for command in input_commands_list:
                if command[0] == 'open':
                    Popen(command[1])
                    time.sleep(1) #REMOVE THIS
                    subprocess.run(["wmctrl", "-R", "shrinidhi@computer: ~/project/vaac"]) #REMOVE THIS                    
                elif command[0] == "focus":
                    subprocess.run(["wmctrl", "-R", command[1]])                
                else:
                    c = command[:]
                    c.insert(0,'./vaac_code/executor.sh') # Hardcoded string.
                    subprocess.run(c)