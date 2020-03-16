import csv
#with open("gedit_keyboard_shortcuts.csv","r") as csvfile:

#with open("firefox_keyboard_shortcuts.csv","r") as csvfile:
#with open("terminal_keyboard_shortcuts.csv","r") as csvfile:
#with open("code_keyboard_shortcuts.csv","r") as csvfile:
#with open("keyboard_shortcuts.csv","r") as csvfile:

words_file = open("words.csv","r")	
shortcuts_file = open("../data/keyboard_shortcuts.csv","r")
words = csv.reader(words_file)   
shortcuts = list(csv.reader(shortcuts_file))
output = open("output","w")
for line in words:
	for shortcut in shortcuts:
		if line[0] in shortcut[0]:
			output.write(line[0]+","+str(shortcut)+"\n")
	output.write("__________________________________________________\n")
