from vaac_code.extractor import extractor
from vaac_code.executor import executor
import subprocess

s = subprocess.getoutput("xdotool getwindowfocus getwindowname")

extractorObj = extractor()
executorObj = executor(s)

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
	print(">",phrase)	
	if phrase != "EXIT":		
		command = extractorObj.find_commands(phrase)
		executorObj.run(command)		
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