# extract all words
# generate grammar
# generate other possible sentences so that the frequencies match.
import csv
from collections import Counter

import nltk
from nltk import CFG
from nltk.parse.generate import generate

f = list(csv.reader(open("config/firefox.csv")))
phrases = [item[0] for item in f]
set_of_rules = Counter()
bag = dict()

for phrase in phrases:
    text = nltk.word_tokenize(phrase)
    pos_tags = nltk.pos_tag(text)
    for word, tag in pos_tags:
        if tag in bag:
            bag[tag].add(word)
        else:
            bag[tag] = set([word])
        # print(word, bag[tag])
    tags = tuple([tag for _, tag in pos_tags])
    set_of_rules[tags] += 1

rules = []

for tags, _ in set_of_rules.most_common():
    string = 'S -> '
    for tag in tags:
        string += tag + ' '
    rules.append(string.strip())

print(rules)
grammar_string = '\n'.join(rules)
print(grammar_string)

grammar = CFG.fromstring(grammar_string)
print(grammar)
print(bag)

print("Generated sentences")
for sentence in generate(grammar, n=10):
    print(sentence)
