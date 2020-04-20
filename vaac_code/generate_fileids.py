import csv
import glob
import re
from pathlib import Path
'''This script simply generates files ids and transcription for all recordings in the recordings folder. 
The test size will be one recording: a tiny amount compared to thousands in the train size.
The test train split is highly imbalanced, as we decide to train the model with all the data, and put only one small recording for testing. This is because it is more important for the model to train on all recorded occurences, than to have a better sense of the wer generated during training. 
This decision is purely based speculation(and has given good results), and you can use the test_train_split script to split the fileids and transcription files to any ratio you desire.
'''
modeldir = 'vaac_model'

test_fileids = modeldir+"/etc/"+modeldir+"_test.fileids"
test_transcription = modeldir+"/etc/"+modeldir+"_test.transcription"
words = sorted(glob.glob('./recordings/words/*'))
for word in words[:1]:
    with open(test_fileids,'w') as test_fileids_file, open(test_transcription,'w') as test_transcription_file:
        for file in sorted(glob.glob(f'{word}/*')):
            # To remove .wav extention
            fileid = file.replace('./recordings/','')[:-4] +'\n'
            transcription = f'<s> {Path(word).stem} </s> ({Path(file).stem})\n'
            test_fileids_file.write(fileid)
            test_transcription_file.write(transcription)

train_fileids = modeldir+"/etc/"+modeldir+"_train.fileids"
train_transcription = modeldir+"/etc/"+modeldir+"_train.transcription"
for word in words[1:]:
    with open(train_transcription,'a') as transcriptionfile, open (train_fileids,'a') as fileidsfile:        
        for file in sorted(glob.glob(f'{word}/*')):
            # To remove .wav extention
            fileid = file.replace('./recordings/','')[:-4] +'\n'
            transcription = f'<s> {Path(word).stem} </s> ({Path(file).stem})\n'
            fileidsfile.write(fileid)
            transcriptionfile.write(transcription)

folders = sorted(glob.glob('./recordings/corpus/*'))
for folder in folders:
    corpusfile_path = f'./corpus/{Path(folder).stem}'
    with open(corpusfile_path,'r') as corpusfile, open(train_transcription,'a') as transcriptionfile, open (train_fileids,'a') as fileidsfile:
        corpus = list(csv.reader(corpusfile))
        for file in sorted(glob.glob(f'{folder}/*')):
            # To remove .wav extention
            fileid = file.replace('./recordings/','')[:-4] +'\n'
            lst = re.findall(r'\d+', Path(file).stem)
            n = int(lst[0])
            transcription = f'<s> {corpus[n][0]} </s> ({Path(file).stem})\n'
            fileidsfile.write(fileid)
            transcriptionfile.write(transcription)