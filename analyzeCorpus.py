import csv
import configparser
from collections import Counter
import glob


class analyseCorpus:
    def __init__(self, min_word_freq, max_word_freq):
        self.min_word_freq = min_word_freq
        self.max_word_freq = max_word_freq
        file_paths = glob.glob('corpus/*')
        print(file_paths)
        self.phrases = []
        for path in file_paths:
            with open(path, 'r') as corpus_file:
                self.phrases.extend(
                    [phrase[0].split() for phrase in list(
                        csv.reader(corpus_file))])
        print('Total corpus length:', len(self.phrases))
        self.count_words()
        self.write_counts()
        self.cover_config()
        self.check_counts()

    def count_words(self):
        '''stores word frequencies in self.counter'''
        self.counter = Counter()
        for phrase in self.phrases:
            for word in phrase:
                self.counter[word] += 1

    def write_counts(self):
        with open('./analytics/corpus_counts.csv', 'w') as corpus_counts:
            for word, freq in self.counter.most_common()[::-1]:
                corpus_counts.write(word+','+str(freq)+'\n')

    def cover_config(self):
        with open('./analytics/counts_summary.csv', 'r') as config_counts_file:
            config_counts = [item[0]
                             for item in list(csv.reader(config_counts_file))]

        not_covered_list = []
        for word in config_counts:
            if word not in self.counter:
                not_covered_list.append(word)

        if not_covered_list == []:
            return
        print("List of words in config not in corpus:")
        for word in not_covered_list:
            print(word)

    def check_counts(self):

        imbalanced = []
        for word, freq in self.counter.most_common():
            if freq < self.min_word_freq:
                imbalanced.append(['lower:', word, freq])
            if freq > self.max_word_freq:
                imbalanced.append(['higher:', word, freq])

        if imbalanced == []:
            return

        print('List of words with imbalanced frequencies:')
        print('Words with frequencies lower and higher than')
        print('Minimum word frequency:', self.min_word_freq)
        print('Maximum word frequency:', self.max_word_freq)
        print('are tagged lower and higher.')
        for item in imbalanced:
            print(item)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('./config/vaac_config')

    min_word_freq = config.getint('CORPUS', 'min_word_freq')
    max_word_freq = config.getint('CORPUS', 'max_word_freq')

    analyseCorpus(min_word_freq, max_word_freq)
