from vaac_code.extractor import extractor
from vaac_code.executor import executor
import subprocess

s = subprocess.getoutput("xdotool getwindowfocus getwindowname")

extractorObj = extractor()
executorObj = executor(s)

while True:
	inputString = input("> ")
	if inputString != "exit":		
		command = extractorObj.find_commands(inputString)						
		executorObj.run(command)		
	else:
		break
