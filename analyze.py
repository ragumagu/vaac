from collections import Counter
import csv

#This script:
#1. Extracts commands phrases from data/keys, and stores them in files #commands_phrases and commands_applications_phrases.


def write_unique_words(phrases, words_file):
    s = set()    
    for elem in phrases:
        for e in elem.split():
            s.add(e)    
    unique_words_list = sorted(s)    
    for w in unique_words_list:
        words_file.write(w+"\n")
    return unique_words_list

def count_words(l, o):
    c = Counter()
    for line in l:        
        for word in line.split():
            c[word] += 1
    c_list = sorted(c.items(), key=lambda pair: pair[1], reverse=True)
    for item in c_list:
        o.write(item[0]+","+str(item[1])+"\n")
    return c


def sum_freq_c(phrase, counter):
    sum = 0
    for word in phrase.split():
        sum += counter[word]
    return sum

def weight(l, counter):
    w = []
    i = 0
    for phrase in l:
        w.append((i, len(phrase.split()), sum_freq_c(phrase, counter)))
        i += 1
    return w

def sort_weights(weights):
    sort_spec = ((1, False), (2, True))
    for index, reverse_value in sort_spec[::-1]:
        weights.sort(key=lambda x: x[index], reverse=reverse_value)

def write_partitions(counter,phrases,output):    
    for word in counter.most_common():    
        for phrase in phrases:            
            p = phrase.split()
            if word[0] in p:                                
                output.write(word[0]+","+phrase+"\n")
        output.write("__________________________________________________\n")    

read = "r"
write = "w"
files = ["./data/keys/code_keyboard_shortcuts.csv", "./data/keys/firefox_keyboard_shortcuts.csv", "./data/keys/gedit_keyboard_shortcuts.csv",
    "./data/keys/general_keyboard_shortcuts.csv", "./data/keys/nautilus_keyboard_shortcuts.csv", "./data/keys/terminal_keyboard_shortcuts.csv"]
apps = ["CODE", "FIREFOX", "GEDIT", "", "NAUTILUS", "TERMINAL"]

commands_phrases_string = "./analytics/commands_phrases.txt"
commands_applications_phrases_string = "./analytics/commands_applications_phrases.txt"


# Writing commands_phrases and commands_applications_phrases files.
commands_phrases = open(commands_phrases_string, write)
commands_applications_phrases = open(commands_applications_phrases_string,write)

i = 0
for filename in files:
    f = open(filename, "r")
    for line in f:
        l = line.split(",")
        commands_phrases.write(l[0]+"\n")
        commands_applications_phrases.write(l[0]+" "+apps[i]+"\n")
    i += 1

commands_phrases.close()
commands_applications_phrases.close()

commands_phrases_list = [item[0] for item in list(csv.reader(open(commands_phrases_string, read)))]
commands_applications_phrases_list = [item[0] for item in list(csv.reader(open(commands_applications_phrases_string,read)))]

# Writing unique words files.
commands_words = "./analytics/commands_words"
commands_applications_words = "./analytics/commands_applications_words"

unique_c_words = write_unique_words(
    commands_phrases_list, open(commands_words, write))
unique_c_a_words = write_unique_words(commands_applications_phrases_list, open(commands_applications_words, write))

# Writing commands_counts and commands_application_counts files.
commands_counts = open("./analytics/commands_counts.csv", write)
commands_applications_counts = open(
    "./analytics/commands_applications_counts.csv", write)

c_count = count_words(commands_phrases_list, commands_counts)
c_a_count = count_words(commands_applications_phrases_list, commands_applications_counts)
commands_counts.close()
commands_applications_counts.close()

# Sorting commands by weight.
weight_c = weight(commands_phrases_list, c_count)
weight_c_a = weight(commands_applications_phrases_list, c_a_count)

sort_weights(weight_c)
sort_weights(weight_c_a)

sorted_commands = open("./analytics/sorted_commands", write)
sorted_commands_a = open("./analytics/sorted_commands_a", write)

for i in range(len(weight_c)):
    sorted_commands.write(commands_phrases_list[weight_c[i][0]]+"\n")
    sorted_commands_a.write(commands_applications_phrases_list[weight_c[i][0]]+"\n")

sorted_commands.close()
sorted_commands_a.close()

sorted_commands_applications = open("./analytics/sorted_commands_applications", write)
for i in range(len(weight_c)):
    sorted_commands_applications.write(commands_applications_phrases_list[weight_c_a[i][0]]+"\n")
sorted_commands_applications.close()
# The following generates partitions commands_partitions and commands_applications_partitions.

partitions = open("./analytics/commands_partitions", write)
partitions_a = open("./analytics/commands_applications_partitions", write)
write_partitions(c_count,commands_phrases_list,partitions)
write_partitions(c_a_count,commands_applications_phrases_list,partitions_a)
partitions.close()
partitions_a.close()

# The following will generate the corpus file.
sorted_commands = list(csv.reader(open("./analytics/sorted_commands", read)))

list_of_commands = [item for item in apps if item != ""]

for item in sorted_commands:    
    if item[0] not in list_of_commands:
        list_of_commands.append(item[0])

text_corpus_file = open("./analytics/vaac_corpus",write)
for item in list_of_commands:
    text_corpus_file.write(item+"\n")
text_corpus_file.close()

# Verify that every word in commands_applications_phrases is in corpus file.
text_corpus_list = list(csv.reader(open("./analytics/vaac_corpus",read)))

s1 = set()    
for elem in commands_applications_phrases_list:
    for e in elem.split():
        s1.add(e)

s2 = set()    
for elem in text_corpus_list:    
    for e in elem[0].split():
        s2.add(e)

if s1 != s2:
    print("The phrases list and corpus are not same. Please check the data.")


