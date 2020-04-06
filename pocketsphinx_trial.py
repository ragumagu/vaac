from multiprocessing import Process, Value, Manager
import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = "vaac_model"

'''
class RecognizedCommands:
    def __init__(self):
        self.commands = []
        self.index = -1

    def __iadd__(self, string):
        self.commands.append(string)
        self.index += 1
        print("In iadd", string)
        print('In iadd', self.commands,self.index)
        return self
'''

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
                            # yield self                            
                            self.recognized_commands.append(str(self))
                            yield self
                            # print(self,self.recognized_commands)
                            #print("In while (1)")

                    elif self.in_speech != self.get_in_speech():
                        self.in_speech = self.get_in_speech()
                        if not self.in_speech and self.hyp():
                            with self.end_utterance():
                                # yield self                                
                                self.recognized_commands.append(str(self))
                                yield self
                                # print(self,self.recognized_commands)
                                #print("In while (2)")


'''
print("> ",end="",flush=True)
for phrase in speech:
    print(str(phrase),end=" ")    
    x = input()
    print("Got x:",str(phrase),x)
    print("> ",end="",flush=True)
'''
'''
vs = vaac_speech()
while 1:
    print("> ",end="",flush=True)    
    x = input()    
    phrase = vs.get_one_command()
    print("Got x:",str(phrase),x)    
    '''

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

ch = getch()

def run_pocketsphinx(rc,inputchars):
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
        for char in str(phrase):
            inputchars.append(char)
        newlen = len(rc)
        if newlen > rclen:            
            rclen = newlen
            print("\r"+"".join(inputchars),end="")
        inp = "".join(inputchars)
        if "EXIT" in inp:
            break


def run_cmdline(rc,inputchars):
    #print("THREAD2")    
    rclen = len(rc)
    while 1:
        #print("THREAD2> ", end="", flush=True)        
        #x = input("Thread2> ")
        
        #print("x:",x,type(x),repr(x),x.isalnum())
        #print("string",string,repr(string))
        
        x = getch()
        if x.isalnum():
            #print("in if")
            inputchars.append(x)
            print("\r"+"".join(inputchars),end="")
        else:
            #print("in else")
            #print(string)
            print()
            if "exit" in "".join(inputchars):
                break
            for i in range(len(inputchars)):
                inputchars.pop()
        

if __name__ == '__main__':
    manager = Manager()
    rc = manager.list()
    inputchars = manager.list()
    p1 = Process(target=run_pocketsphinx, args=(rc,inputchars,))
    p1.start()
    #p2 = Process(target=run_cmdline,args=(rc,))
    run_cmdline(rc,inputchars,)
    #p2.start()
    p1.join()
    #p2.join()
