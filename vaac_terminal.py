from vaac_code.extractor import extractor
from vaac_code.executor import executor

extractorObj = extractor()
executorObj = executor()

while True:
	inputString = input("> ")
	if inputString != "exit":		
		command = extractorObj.find_commands(inputString)						
		executorObj.run(command)
	else:
		break
