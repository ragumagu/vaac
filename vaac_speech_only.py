from vaac_code.extractor import Extractor
from vaac_code.executor import Executor
from vaac_code.window_manager import WindowManager
import subprocess

s = subprocess.getoutput("xdotool getwindowfocus getwindowname")
wm = WindowManager(s)
wm.resize_all()
extractorObj = Extractor(wm)
executorObj = Executor(wm)

import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = "vaac_model"

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'vaac_model.cd_cont_2000'),
    lm=os.path.join(model_path, 'vaac_model.lm.DMP'),
    dic=os.path.join(model_path, 'vaac_model.dic')
)

for phrase in speech:
	phrase = str(phrase)	
	print("> ",phrase)
	if phrase != "EXIT":		
		command = extractorObj.find_commands(phrase)
		executorObj.run(command)
		print("Ready...")	

	else:
		break
	
	

'''

while True:
	inputString = input("> ")
	if inputString != "exit":		
		command = extractorObj.find_commands(inputString)						
		executorObj.run(command)		
	else:
		break
'''
