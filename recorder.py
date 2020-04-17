import subprocess
from subprocess import Popen

from vaac_code.recorder import GetchUnix, RecordingManager

getch = GetchUnix()
rm = RecordingManager()
phrase = rm.getNext()

def printPhrase():
    if phrase is not None:
        print("Read:\n\t",phrase)

print("___________________________________")
printPhrase()
print("Press j to start recording.",end="",flush=True)

while phrase is not None:
    ch = getch()
    if ch == "j" or ch == "s":
        # Recording
        print("\rRecording... Press k to stop recording.",end="")
        p = Popen(['exec arecord -f S16_LE -r 16000 /tmp/test.wav'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True)
        previous = ch
    elif (ch == "k" and previous == "j") or (ch == "d" and previous == "s"):
        # stop recording
        print("\rRecorded. Press l to save, ; otherwise.",end="")
        p.kill()
        previous = ch
    elif (ch == "l" and previous == "k") or (ch == "f" and previous == "d"):
        # save
        print("\rSaving..."+" "*30)
        rm.save()
        phrase = rm.getNext()
        if phrase is None:
            break
        printPhrase()
        print("\rPress j to start recording.",end="")
        previous = ch
    elif (ch == ";" and previous == "k") or (ch == "g" and previous == "d"):
        printPhrase()
        print("\rPress j to start recording.",end="")
    else:
        print()
        break

if phrase is None:
    print("\nHurray! You finished recording the corpus!")
