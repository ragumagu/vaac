'''This is the vaac recorder module. It has a recordings manager which keeps track of corpus recording progress.
'''
import csv
import json
import os
import re
import glob
from pathlib import Path
import subprocess
import configparser

# The _GetchUnix class replicates the functionality of the getch() method.
class GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class RecordingManager:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config/vaac_config')
        self.min_word_freq = config.getint('RECORDINGS','min_word_freq')
        self.min_command_freq = config.getint('RECORDINGS', 'min_command_freq')

        self.recording_words = True
        self.word = ''
        self.corpus = ''
        self.n = 0
        self.i = 0

    def getWords(self):
        with open('analytics/corpus_counts.csv','r') as wordsCountsFile:
            words = [item[0] for item in list(csv.reader(wordsCountsFile))]

        for word in words:
            for i in range(self.min_word_freq):
                recpath = f'recordings/words/{word}/{word}_{i}.wav'
                #print("DEBUG: searching for",recpath)
                if not os.path.exists(recpath):
                    self.word = word
                    self.i = i
                    return self.word

    def getPhrases(self):
        corpusfiles = sorted(glob.glob('./corpus/*'))
        for corpusfilestr in corpusfiles:
            corpusname = Path(corpusfilestr).stem
            with open(corpusfilestr,'r') as corpusfile:
                corpus = list(csv.reader(corpusfile))
            #print("DEBUG:getPhrases checking from",self.n, 'to', len(corpus))
            for n in range(self.n,len(corpus)):
                for i in range(self.min_command_freq):
                    recpath = f'recordings/corpus/{corpusname}/recording{n}_{i}.wav'
                    #print("DEBUG: searching for",recpath)
                    if not os.path.exists(recpath):
                        self.corpus = corpusname
                        self.n = n
                        self.i = i
                        return corpus[n][0]

    def getNext(self):
        if self.recording_words:
            result = self.getWords()
            if result is None: # has completed recording words
                self.recording_words = False
                return self.getPhrases()
            else:
                return result
        else:
            return self.getPhrases()

    def save(self):
        recpath = ''
        if self.recording_words:
            dirpath = f'recordings/words/{self.word}/'
            recpath = f'recordings/words/{self.word}/{self.word}_{self.i}.wav'
        else:
            dirpath = f'recordings/corpus/{self.corpus}/'
            recpath = f'recordings/corpus/{self.corpus}/recording{self.n}_{self.i}.wav'
        subprocess.run(['mkdir','-p',dirpath])
        subprocess.run(['mv','/tmp/test.wav',recpath])
        print("DEBUG:moving to",recpath)
