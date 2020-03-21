import csv
import re
from collections import Counter
files = ["./data/keys/code_keyboard_shortcuts.csv","./data/keys/firefox_keyboard_shortcuts.csv","./data/keys/gedit_keyboard_shortcuts.csv","./data/keys/general_keyboard_shortcuts.csv","./data/keys/nautilus_keyboard_shortcuts.csv","./data/keys/terminal_keyboard_shortcuts.csv"]
apps = ["CODE","FIREFOX","GEDIT","","NAUTILUS","TERMINAL"]

# The following concats all the command phrases in all the files.
commands_phrases = open("./analytics/commands_phrases.txt","w")
for f in files:
    f = open(f,"r")
    f = csv.reader(f)
    for line in f:
        commands_phrases.write(line[0]+"\n")    
commands_phrases.close()

commands_applications_phrases = open("./analytics/commands_applications_phrases.txt","w")

# The following concats all the command phrases and app names in all the files.
i = 0
for f in files:
    f = open(f,"r")
    f = csv.reader(f)                
    for line in f:
        commands_applications_phrases.write(line[0]+" "+apps[i]+"\n")
    i += 1
    
commands_applications_phrases.close()

commands_phrases = open("./analytics/commands_phrases.txt","r")
commands_applications_phrases = open("./analytics/commands_applications_phrases.txt","r")

def get_words(f):
    for line in f:
        for word in line.split():
            yield word


commands_words = open("./analytics/commands_words","w")
unique_c_words = sorted(set(get_words(commands_phrases)))
for w in unique_c_words:
    commands_words.write(w+"\n")
commands_words.close()

commands_applications_words = open("./analytics/commands_applications_words","w")

unique_c_a_words = sorted(set(get_words(commands_applications_phrases)))
for w in unique_c_a_words:
    commands_applications_words.write(w+"\n")
commands_applications_words.close()

c = Counter()
for line in open("./analytics/commands_phrases.txt","r"):
    for word in line.split():
        c[word] += 1
c_list = sorted(c.items(), key=lambda pair: pair[1], reverse=True)

commands_counts = open("./analytics/commands_counts","w")

for item in c_list:
    commands_counts.write(item[0]+","+str(item[1])+"\n")
commands_counts.close()

c_a = Counter()
for line in open("./analytics/commands_applications_phrases.txt","r"):
    for word in line.split():
        c_a[word] += 1
c_a_list = sorted(c_a.items(), key=lambda pair: pair[1], reverse=True)

commands_applications_counts = open("./analytics/commands_applications_counts","w")

for item in c_a_list:
    commands_applications_counts.write(item[0]+","+str(item[1])+"\n")
commands_applications_counts.close()

def sum_freq_c(line):
    sum = 0
    for word in line.split():
        sum += c[word] 

def sum_freq_c_a(line):
    sum = 0
    for word in line.split():
        sum += c_a[word]

c_weights = []
for line in commands_phrases
