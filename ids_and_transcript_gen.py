import os
import re
import csv
fileids = open("./data/pocketsphinx_files/recordings.fileids","w")
transcription = open("./data/pocketsphinx_files/recordings.transcription","w")
commands_file = open("./rough_work/commands_applications.txt")
commands = list(csv.reader(commands_file))

files = os.listdir("./data/recordings")
files.sort()

for f in files:
    lis = re.findall(r'\d+', f)     
    if len(lis) == 2:
        n = lis[0]
        i = lis[1]
        fname = "./data/recordings/recording"+n+"_"+i
        #fname = "recording"+n+"_"+i
        fileids.write(fname+"\n")
        transcription.write("<s> "+commands[int(n)][0].upper()+" </s> ("+fname+")\n")

'''
#Logic to extract files:
#If recording(n)_(i)
fname = fname = "./data/recordings/recording"+str(n)+"_"+str(i)
fileids.write(fname+"\n")
transcription.write("<s> "+commands[n][0].upper()+" </s> ("+fname+")\n")
'''