import os
import argparse
import csv

desc = '''This script copies recordings from the recordings folder into the models set of recordings.'''

parser = argparse.ArgumentParser(description=desc)
parser.add_argument("--corpus",required=True,type=str, help="Takes path to corpus file.")
parser.add_argument("--modeldir",required=True,type=str, help="Takes path to model directory.")

args = parser.parse_args()
corpus_file_string = args.corpus
model_dir_string = args.modeldir
corpus_file = open(corpus_file_string)
corpus = list(csv.reader(corpus_file))

fileids = open(model_dir_string+"/working/"+model_dir_string+".fileids","a")
transcription = open(model_dir_string+"/working/"+model_dir_string+".transcription","a")

n = 0
for word in corpus:
    filesdir = str("./recordings/"+word[0]+"/").lower()
    files = os.listdir(filesdir)    
    files.sort()   
    i = 0     
    for f in files:
        filename = "word"+str(n)+"_"+str(i)
        os.system("cp ./recordings/"+word[0].lower()+"/"+f+" "+model_dir_string+"/recordings/"+filename+".wav")
        fileids.write(filename+"\n")
        transcription.write("<s> "+corpus[int(n)][0].upper()+" </s> ("+filename+")\n")

        i += 1    
    n += 1
