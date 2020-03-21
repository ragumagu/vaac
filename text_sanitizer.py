import argparse
import csv
import re
desc = '''This program sanitizes the input commands csv files, removes any extraneous characters, and converts input to proper representation. This sanitizer also and verifies if each keystroke is a valid X keysym string.
'''
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("--csv",required=True,type=str, help="Takes path to csv file.")

args = parser.parse_args()
csv_file_string = args.csv
input_file = open(csv_file_string,"r")
csv_file = csv.reader(input_file)

x_keysym_file = open("./data/keys/xdotool_keysym_names.csv")
keysym = list(csv.reader(x_keysym_file))

output = open("output","w")

def get_repr(string):
    s2 = ""
    keys = string.split("+")
    for key in keys:
        for i in range(len(keysym)):
            if key.lower() == keysym[i][0].lower() and len(key) != 1:                
                s2 += keysym[i][0]+"+"
                break
            elif key == keysym[i][0] and len(key) == 1:
                s2 += key.lower()+"+"                
                break
    s2 = s2[:-1]
    return s2

for sentence in csv_file:
    s1 = re.sub('[\W_]+', ' ', sentence[0])
    s1 = s1.upper()
    strings = sentence[1].split(" ")
    s2 = ""
    for string in strings:
        s2 = s2+ get_repr(string) + " "
    s2 = s2[:-1]
    output.write(s1+","+s2+"\n")

output.close()