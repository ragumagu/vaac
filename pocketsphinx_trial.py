import os
from multiprocessing import Process, Value, Manager
from pocketsphinx import LiveSpeech, get_model_path

model_path = "/home/shrinidhi/project/vaac/vaac_model"

class VaacSpeech(LiveSpeech):
    def __init__(self, **kwargs):
        self.recognized_commands = kwargs.pop('rcobj')
        super(VaacSpeech, self).__init__(**kwargs)

    def __iter__(self):
        with self.ad:
            with self.start_utterance():
                while self.ad.readinto(self.buf) >= 0:
                    self.process_raw(self.buf, self.no_search, self.full_utt)
                    if self.keyphrase and self.hyp():
                        with self.end_utterance():
                            self.recognized_commands.append(str(self))
                            yield self

                    elif self.in_speech != self.get_in_speech():
                        self.in_speech = self.get_in_speech()
                        if not self.in_speech and self.hyp():
                            with self.end_utterance():
                                self.recognized_commands.append(str(self))
                                yield self



### The _GetchUnix function replicates the functionality of the getch() method.

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

#ch = getch()

def run_pocketsphinx(rc,inputchars):
    #print("in run_ps")
    speech = VaacSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=os.path.join(model_path, 'vaac_model.cd_cont_2000'),
        lm=os.path.join(model_path, 'vaac_model.lm.DMP'),
        dic=os.path.join(model_path, 'vaac_model.dic'),
        rcobj=rc
    )
    rclen = 0
    
    for phrase in speech: 
        for char in str(phrase).lower():
            inputchars.append(char)
        newlen = len(rc)
        inp = (" " + "".join(inputchars)).strip()
        if newlen > rclen:                        
            rclen = newlen
            print("\r> "+inp,end="")        
        if "exit" in inp:
            print()
            break

def run_cmdline(rc,inputchars):
    #print("in run_cmdline")
    rclen = len(rc)    
    while 1:         
        inp = "".join(inputchars)
        print("\r> "+inp+"\033[K",end="")
        x = getch()
        print("ord(x)",ord(x))

        if ord(x) >= 32 and ord(x) <= 126:            
            inputchars.append(x)            
            print("\r> "+inp+"\033[K",end="")
        elif ord(x) == 127: #Backspace
            try:
                inputchars[-1] = ""
                del inputchars[-1]
            except:
                pass
            print("\r> "+inp+"\033[K",end="")
        elif repr(x) == '\x1b'
        else:
            print()
            if "exit" in "".join(inputchars):
                break
            for i in range(len(inputchars)):
                inputchars.pop()
            print("> ",end="")
        

if __name__ == '__main__':
    manager = Manager()
    rc = manager.list()
    inputchars = manager.list()
    p1 = Process(target=run_pocketsphinx, args=(rc,inputchars,))
    p1.start()    
    run_cmdline(rc,inputchars,)    
    p1.join()
    
