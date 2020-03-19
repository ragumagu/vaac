from subprocess import Popen, PIPE
import subprocess
import time
print("This prompts a command and records it in a file.")
print("Read the prompted command vocally into the microphone.")
print("Press j to start recording.")
print("Press k to stop recording.")
print("Press l to store recording.")
print("Press ; to re-record without storing.")
print("Press n for next command.")
print("Press p for previous command.")
print("Press e or any other key to exit.")
print("Pressing unexpected keys will terminate the program.")
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

getch = _GetchUnix()

input_strings = ['copy firefox','paste gedit']
n = 0
i = 0

print("___________________________________")
print("Read:", input_strings[n])
print("Press j to start recording.",end="",flush=True)

previous = ""
while True:                
    command = getch()
    if command == "j":
        # Recording
        print("\rRecording... Press k to stop recording.",end="")
        
        p = Popen(['exec arecord -f S16_LE -r 16000 test.wav'],stdin=PIPE, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True)
        previous = command

    elif command == "k" and previous == "j":        
        # stop recording
        print("\rRecorded. Press l to save, ; otherwise.",end="")
        time.sleep(0.5)
        p.kill()
        time.sleep(0.5)
        previous = command

    elif command == "l" and previous == "k":
        # save
        print("Saving...")
        fname = "./data/recordings/recording"+str(n)+"_"+str(i)+".wav"
        subprocess.run(['mv','test.wav',fname])
        i += 1
        print("\nRead:", input_strings[n])
        print("\rPress j to start recording.",end="")
        previous = command

    elif command == ";" and previous == "k":
        #print("\r")
        print("\nRead:", input_strings[n])
        print("\rPress j to start recording.",end="")        
        continue
    elif command == "n" and n < (len(input_strings)-1) and (previous == "l" or previous == ";"):
        n += 1
        print("\nRead:", input_strings[n])
        print("\rPress j to start recording.",end="")        
        continue
    elif command == "p" and n > 0 and (previous == "l" or previous == ";"):
        n -= 1  
        print("\nRead:", input_strings[n])
        print("\rPress j to start recording.",end="")        
        continue  
    else:
        print()
        break
