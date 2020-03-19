import csv
#with open("gedit_keyboard_shortcuts.csv","r") as csvfile:

#with open("firefox_keyboard_shortcuts.csv","r") as csvfile:
#with open("terminal_keyboard_shortcuts.csv","r") as csvfile:
#with open("code_keyboard_shortcuts.csv","r") as csvfile:
#with open("keyboard_shortcuts.csv","r") as csvfile:

'''
#The following generates partitions.
words_file = open("wordcloud_commands_applications.csv","r")	
shortcuts_file = open("commands and applications.txt","r")
words = csv.reader(words_file)   
shortcuts = list(csv.reader(shortcuts_file))
output = open("output","w")
for line in words:
	for shortcut in shortcuts:
		if line[0] in shortcut[0]:
			output.write(line[0]+","+str(shortcut)+"\n")
	output.write("__________________________________________________\n")
'''

'''
shortcuts_file = open("../data/shortcuts/general_keyboard_shortcuts.csv","r")
output = open("output","w")
shortcuts = csv.reader(shortcuts_file)
for line in shortcuts:
	output.write(line[0]+"\n")
'''

output = open("output","w")
words_file = open("wordcloud_commands_applications.csv","r")	
words = csv.reader(words_file)   
for line in words:
	output.write(line[0]+"\n")