import argparse
import csv
import os
import re
parser = argparse.ArgumentParser(description="This script generates the fileids and transcription files.")
parser.add_argument("--modelname",required=True,type=str, help="Takes name of model. It is not a path.")


args = parser.parse_args()
model_name = args.modelname

fileids = open(model_name+"/working/"+model_name+".fileids","w")
transcription = open(model_name+"/working/"+model_name+".transcription","w")
corpus_file = open(model_name+"/"+model_name+"_corpus")
corpus = list(csv.reader(corpus_file))

files = os.listdir(model_name+"/recordings/")
#files.sort()

for f in files:
    lis = re.findall(r'\d+', f)     
    if len(lis) == 2:
        n = lis[0]
        i = lis[1]
        fname = "recording"+n+"_"+i        
        fileids.write(fname+"\n")
        transcription.write("<s> "+corpus[int(n)][0].upper()+" </s> ("+fname+")\n")

fileids.close()
transcription.close()
