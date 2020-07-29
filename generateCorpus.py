import csv
import nltk


def make_pairs(phrases):
    ''' Returns each pair of words that occur in the phrases list'''
    for phrase in phrases:
        words = phrase.split()
        for i in range(len(words) - 1):
            yield (words[i], words[i+1])


f = list(csv.reader(open("config/firefox.csv")))
phrases = [item[0] for item in f]
print("Length of config:", len(phrases))

pairs = make_pairs(phrases)
word_dict = {}
for word_1, word_2 in pairs:
    if word_1 in word_dict.keys() and word_2 not in word_dict[word_1]:
        word_dict[word_1].append(word_2)
    else:
        word_dict[word_1] = [word_2]

# testing if all word pairs are there
for word_1, word_2 in pairs:
    assert word_2 in word_dict[word_1]

firsts = sorted(list(set([item.split()[0] for item in phrases])))
lasts = sorted(list(set([item.split()[-1] for item in phrases])))

# for key, value in word_dict.items():
#     print(key, value)

sentences = []
for word in firsts:
    sentences.append([word])

for _ in range(4):
    buffer = []
    for sentence in sentences:
        if sentence[-1] in word_dict:
            for word in word_dict[sentence[-1]]:
                buffer.append(sentence+[word])
    for elem in buffer:
        if elem not in sentences:
            sentences.append(elem)

sentences.sort()

# for sentence in sentences:
#     if sentence[-1] not in lasts and len(sentence) != 1:
#         print(" ".join(sentence), sentence)
        # sentences.remove(sentence)

# for sentence in sentences:
#    print(" ".join(sentence))


pos_frames = {}
for index, phrase in enumerate(phrases):
    tokens = nltk.word_tokenize(phrase)
    pos_tags = nltk.pos_tag(tokens)
    frame = tuple([pos_tag for word, pos_tag in pos_tags])
    print(phrase, frame)
    if frame not in pos_frames.keys():
        pos_frames[frame] = [index]
    else:
        pos_frames[frame].append(index)

for sentence in sentences:
    tokens = nltk.word_tokenize(" ".join(sentence))
    pos_tags = nltk.pos_tag(tokens)
    frame = tuple([pos_tag for word, pos_tag in pos_tags])

    if frame not in pos_frames.keys():
        print(" ".join(sentence), sentence)
