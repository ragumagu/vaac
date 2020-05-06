# extract all words
# generate grammar
# generate other possible sentences so that the frequencies match.

import csv
from timeit import default_timer as timer

from fuzzywuzzy import fuzz

app_names = [
    'code', 'firefox', 'gedit',
            'general', 'gnome-terminal', 'nautilus',
            'keys',
]
files_map = {}
for app_name in app_names:
    path = f'./data/keys/{app_name}.csv'
    with open(path, 'r') as dfile:  # data file
        files_map[app_name] = [item[0] for item in list(csv.reader(dfile))]


def binarySearch(A, X):
    ''' Returns index i if A[i] == X, else returns -1.'''
    low, high = 0, len(A)
    while low < high:
        i = low + (high - low) // 2
        if X == A[i]:
            return i
        elif X > A[i]:
            low = i + 1
        else:  # X < A[i]
            high = i
    return -1


def match(A, pattern):
    matched_command = max(A,
                          key=lambda x: fuzz.token_sort_ratio(
                              pattern, x))

    max_ratio = fuzz.token_sort_ratio(pattern, matched_command)
    if max_ratio == 100:
        result = [matched_command]
        result.insert(0, 'key')
        return result
    else:
        return None


start = timer()
length = 0
fail_count = 0
for app in app_names:
    length += len(files_map[app])
    for i in files_map[app]:
        res = binarySearch(files_map[app], i)
        if files_map[app][res] != i:
            print("FAIL", res)
            fail_count += 1

end = timer()
avg = (end - start) / length
print("Binary search Average access time:", avg)
print("len:", length)
print("Fail count:", fail_count)
print("----------------------")

start = timer()
length = 0
fail_count = 0
for app in app_names:
    length += len(files_map[app])
    for i in files_map[app]:
        res = match(files_map[app], i)
        if res is None:
            print("FAIL")
            fail_count += 1

end = timer()
avg = (end - start) / length
print("Fuzzy search Average access time:", avg)
print("len:", length)
print("Fail count:", fail_count)
print("----------------------")
