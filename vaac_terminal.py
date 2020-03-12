from vaac.extractor import extractor
from vaac.executor import executor

extractorObj = extractor()
executorObj = executor()
current_app = ""
while True:
	inputString = input("> ")
	if inputString != "exit":		
		current_app, command = extractorObj.extract(inputString,current_app)
		print("Target application:",current_app)
		print("Command:",command)
		executorObj.run(['key',command[1],current_app])
		#executorObj.run(command)
	else:
		break
