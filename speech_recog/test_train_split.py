import argparse
import csv
import glob
from numpy import floor,ceil,ones,zeros,hstack
import numpy.random as random

desc='''This script splits data into training and test data.'''
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("--modeldir",required=True,type=str, help="Takes path to model directory.")
parser.add_argument("--ratio",required=True,type=float, help="Takes test-train split ratio.")
args = parser.parse_args()
model_dir_string = args.modeldir
ratio = args.ratio

fileids_string = model_dir_string+"/working/"+model_dir_string+".fileids"
transcription_string = model_dir_string+"/working/"+model_dir_string+".transcription"

test_fileids_string = model_dir_string+"/working/"+model_dir_string+"_test.fileids"
train_fileids_string = model_dir_string+"/working/"+model_dir_string+"_train.fileids"
test_transcription_string = model_dir_string+"/working/"+model_dir_string+"_test.transcription"
train_transcription_string = model_dir_string+"/working/"+model_dir_string+"_train.transcription"

fileids = [item[0] for item in list(csv.reader(open(fileids_string,"r")))]
transcription = [item[0] for item in list(csv.reader(open(transcription_string,"r")))]
#print(fileids)
#print(transcription)

test_fileids = open(test_fileids_string,"w")
train_fileids = open(train_fileids_string,"w")
test_transcription = open(test_transcription_string,"w")
train_transcription = open(train_transcription_string,"w")

number_of_recordings = len(fileids)
limit = int(floor(number_of_recordings * ratio))

idx = hstack((ones(limit), zeros(number_of_recordings-limit))) # generate indices
random.shuffle(idx) # shuffle to make training data and test data random

for i in range(number_of_recordings):
    if idx[i] == 1:
        train_fileids.write(fileids[i]+"\n")
        train_transcription.write(transcription[i]+"\n")
    else:
        test_fileids.write(fileids[i]+"\n")
        test_transcription.write(transcription[i]+"\n")
