import csv
from collections import Counter
import glob
from pathlib import Path
# unique words
# unique phrases
# word frequencies
# partitions [word,line,file]
# sort commands by number of words(least first), frequency(most first).

# Do this for all words config/*.csv; all files in corpus/*.

# check if corpus covers csv.
# lm covers csv.
# min_word_freq < word frequencies < max_word_freq

# should write a summary file with all above data.
class Analyze():
    def __init__(self,files):
        lines = []
        for file in files:
            lines.extend([item[0] for item in list(csv.reader(file))])
        self.phrases = [phrase.split() for phrase in lines]
        self.count_words()
        self.sort_phrases()

    def count_words(self):
        '''stores word frequencies in self.counter'''
        self.counter = Counter()
        for phrase in self.phrases:
            for word in phrase:
                self.counter[word] += 1

    def sort_phrases(self):
        '''Sorts phrases by length first (shortest first),
         and sum of word frequencies in phrase second
         (highest sum first).'''
        weights = []
        for idx,phrase in enumerate(self.phrases):
            weights.append(
                (idx,
                len(phrase),
                sum([self.counter[word] for word in phrase]))
            )
        # In the lambda expression,
        # minus implies reverse -> highest first
        self.weights = sorted(weights, key=lambda x: (x[1], -x[2]))

    def write_partitions(self,output):
        for word,_ in self.counter.most_common():
            for phrase in self.phrases:
                if word in phrase:
                    output.write(word+","+' '.join(phrase)+','+"\n")
            output.write('_'*80+'\n')

    def __add__(self,other):
        print('self.phrases len:',len(self.phrases))
        print('other.phrases len:',len(other.phrases))
        self.phrases.extend(other.phrases)
        print('After extending, self.phrases len:',len(self.phrases))
        self.count_words()
        self.sort_phrases()
        return self

if __name__ == "__main__":
    file_names = [Path(item).stem for item in glob.glob('./config/*.csv')]
    print(file_names)
    print('Processing',len(file_names),'files.')

    for app_name in file_names:
        sourcepath = f'./config/{app_name}.csv'
        counts_path = f'./analytics/{app_name}_counts.csv'
        partitions_path = f'./analytics/{app_name}_partitions.csv'

        with open(sourcepath,'r') as inputFile:
            analyzer = Analyze([inputFile])

        with open(counts_path,'w') as countsFile:
            for word,freq in analyzer.counter.most_common():
                countsFile.write(word+','+str(freq)+'\n')

        with open(partitions_path,'w') as partitionsFile:
            analyzer.write_partitions(partitionsFile)

    files = []
    for app_name in file_names:
        sourcepath = f'./config/{app_name}.csv'
        files.append(open(sourcepath,'r'))

    summary = Analyze(files)

    counts_path = './analytics/counts_summary.csv'
    with open(counts_path,'w') as countsFile:
        for word,freq in summary.counter.most_common():
            countsFile.write(word+','+str(freq)+'\n')

    partitions_path = './analytics/partitions_summary.csv'
    with open(partitions_path,'w') as partitionsFile:
        summary.write_partitions(partitionsFile)

    for f in files:
        f.close()