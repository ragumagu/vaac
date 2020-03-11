import subprocess
import platform
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

    def run(self, argslist):
        '''This takes in, a list argument with:
                command[0] = 'key' or 'type' or 'open'
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
        print("Executor run received",argslist)
        if self.platform == 'Linux':
            if argslist[0] == 'open':
                subprocess.run(argslist[1])
            else:
                al = argslist[:]
                al.insert(0,'./vaac/executor.sh') # Hardcoded string.
                subprocess.run(al)
