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


class AnalyzeCSV():
    def __init__(self, names):
        self.sourcepaths = [f'./config/{name}.csv' for name in names]
        if len(names) == 1:
            self.sorted_path = f'./analytics/{names[0]}_sorted.csv'
            self.counts_path = f'./analytics/{names[0]}_counts.csv'
            self.partitions_path = f'./analytics/{names[0]}_partitions.csv'
        else:
            self.sorted_path = f'./analytics/sorted_summary.csv'
            self.counts_path = f'./analytics/counts_summary.csv'
            self.partitions_path = f'./analytics/partitions_summary.csv'

        self.phrases = []
        for source, name in zip(self.sourcepaths, names):
            with open(source, 'r') as file:
                lines = [item[0] for item in list(csv.reader(file))]
                for line in lines:
                    self.phrases.append([line.split(), name])

        self.count_words()
        self.write_counts()
        self.write_partitions()
        self.sort_phrases()
        self.write_sorted()

    def count_words(self):
        '''stores word frequencies in self.counter'''
        self.counter = Counter()
        for phrase in self.phrases:
            for word in phrase[0]:
                self.counter[word] += 1

    def sort_phrases(self):
        '''Sorts phrases by length first (shortest first),
         and sum of word frequencies in phrase second
         (highest sum first), and the phrase itself.'''
        weights = []
        for idx, phrase in enumerate(self.phrases):
            weights.append(
                (idx,
                 len(phrase[0]),
                 sum([self.counter[word] for word in phrase[0]]),
                 phrase[0],)
            )
        # In the lambda expression,
        # minus implies reverse -> highest first
        self.weights = sorted(weights, key=lambda x: (x[1], -x[2], x[3]))

    def write_sorted(self):
        with open(self.sorted_path, 'w') as sortFile:
            for weight in self.weights:
                sortFile.write(
                    str(' '.join(self.phrases[weight[0]][0])) + ','
                    + self.phrases[weight[0]][1] + "\n"
                )

    def write_counts(self):
        with open(self.counts_path, 'w') as countsFile:
            for word, freq in self.counter.most_common():
                countsFile.write(word+','+str(freq)+'\n')

    def write_partitions(self):
        with open(self.partitions_path, 'w') as PartitionsFile:
            for word, _ in self.counter.most_common():
                lst = []
                for phrase in self.phrases:
                    if word in phrase[0]:
                        lst.append([word,phrase[0],phrase[1]])
                lst = sorted(lst,key=lambda x: x[1])
                for line in lst:
                    PartitionsFile.write(
                        line[0] + ','
                        + ' '.join(line[1]) + ','
                        + line[2] + "\n")
                PartitionsFile.write('_'*80+'\n')

if __name__ == "__main__":
    file_names = [Path(item).stem for item in glob.glob('./config/*.csv')]
    print(file_names)
    print('Processing', len(file_names), 'files.')

    # Create analyzeCSV objects for each file
    _ = [AnalyzeCSV([name]) for name in file_names]

    # Create analyzeCSV object for all files
    AnalyzeCSV(file_names)


