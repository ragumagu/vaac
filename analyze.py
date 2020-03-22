from collections import Counter
import csv
def get_words(f):
    for line in f:
        for word in line.split():
            yield word

def write_unique_words(phrases,words):
    unique_words = sorted(set(get_words(phrases)))
    for w in unique_words:
        words.write(w+"\n")
    return unique_words

def count_words(f,o):
    c = Counter()
    for line in f:
        for word in line.split():
            c[word] += 1
    c_list = sorted(c.items(), key=lambda pair: pair[1], reverse=True)
    for item in c_list:
        o.write(item[0]+","+str(item[1])+"\n")
    return c

def sum_freq_c(line,counter):
    sum = 0
    for word in line.split():
        sum += counter[word] 
    return sum

def weight(f,counter):
    w = []
    i = 0
    for line in f:
        w.append((i,len(line.split()),sum_freq_c(line,counter)))
        i += 1
    return w

files = ["./data/keys/code_keyboard_shortcuts.csv","./data/keys/firefox_keyboard_shortcuts.csv","./data/keys/gedit_keyboard_shortcuts.csv","./data/keys/general_keyboard_shortcuts.csv","./data/keys/nautilus_keyboard_shortcuts.csv","./data/keys/terminal_keyboard_shortcuts.csv"]
apps = ["CODE","FIREFOX","GEDIT","","NAUTILUS","TERMINAL"]

commands_phrases = open("./analytics/commands_phrases.txt","w")
commands_applications_phrases = open("./analytics/commands_applications_phrases.txt","w")

i = 0
for filename in files:
    f = open(filename,"r")
    for line in f:
        l = line.split(",")
        commands_phrases.write(l[0]+"\n")
        commands_applications_phrases.write(l[0]+" "+apps[i]+"\n")
    i += 1

read = "r"
write = "w"
commands_phrases = "./analytics/commands_phrases.txt"
commands_applications_phrases = "./analytics/commands_applications_phrases.txt"

commands_words = "./analytics/commands_words"
commands_applications_words = "./analytics/commands_applications_words"
commands_counts = open("./analytics/commands_counts","w")
commands_applications_counts = open("./analytics/commands_applications_counts","w")

unique_c_words = write_unique_words(open(commands_phrases,read),open(commands_words,write))
unique_c_a_words = write_unique_words(open(commands_applications_phrases,read),open(commands_applications_words,write))

c_count = count_words(open(commands_phrases,read),commands_counts)
c_a_count = count_words(open(commands_applications_phrases,read),commands_applications_counts)

weight_c = weight(open(commands_phrases,read),c_count)
weight_c_a = weight(open(commands_applications_phrases,read),c_a_count)

sort_spec = ((1, False), (2, True))
for index, reverse_value in sort_spec[::-1]:
    weight_c.sort(key = lambda x: x[index], reverse=reverse_value)
    weight_c_a.sort(key = lambda x: x[index], reverse=reverse_value)

sorted_commands = open("./analytics/sorted_commands",write)
sorted_commands_a = open("./analytics/sorted_commands_a",write)
commands = list(csv.reader(open(commands_phrases)))
commands_a = list(csv.reader(open(commands_applications_phrases)))
for i in range(len(weight_c)):
    sorted_commands.write(commands[weight_c[i][0]][0]+"\n")
    sorted_commands_a.write(commands_a[weight_c[i][0]][0]+"\n")

sorted_commands_applications = open("./analytics/sorted_commands_applications",write)
commands_a = list(csv.reader(open(commands_applications_phrases)))
for i in range(len(weight_c)):
    sorted_commands_applications.write(commands_a[weight_c_a[i][0]][0]+"\n")

