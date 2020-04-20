import subprocess
from subprocess import Popen
'''This is the Executor module.
	Usage:
		This works on Linux systems with X. Requires wmctrl and xdotool to be installed.
        The run method takes in, a list argument with:
            command[0] = 'key' or 'open' or 'focus'
            command[1] = 'key_stroke_string'
            command[2] = 'target_application_name'
        target_application_name is optional. If not mentioned, the key strokes are directed to current window.
        The key_stroke string is not included, when using 'open' or 'focus'.
        Usage examples:
            # Send key stroke to app:
            >>> executor.run(['key','ctrl+a', 'app'])
            # Open app:
            >>> executor.run(['open','app'])
            # Focus app window.
            >>> executor.run(['focus','app'])
'''

def run(command, wm):
    if command is None:
        return
    elif command[0] == 'open':
        Popen(command[1],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    elif command[0] == 'focus':
        wm.focus(command[1])
    else:
        if len(command) == 3:
            wm.focus(command[2])
        cmd = ['xdotool', command[0]]
        for keystroke in command[1].split():
            cmd.append(keystroke)
        subprocess.run(cmd)