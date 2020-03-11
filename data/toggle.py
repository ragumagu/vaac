import csv
#with open("gedit_keyboard_shortcuts.csv","r") as csvfile:

#with open("firefox_keyboard_shortcuts.csv","r") as csvfile:
#with open("terminal_keyboard_shortcuts.csv","r") as csvfile:
with open("code_keyboard_shortcuts.csv","r") as csvfile:
    reader = csv.reader(csvfile)   
    count = 0 
    for line in reader:
        if " " in line[1]:
            print(line)
            count+=1
    print(count)