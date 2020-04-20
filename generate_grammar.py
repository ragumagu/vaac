import csv
import glob
from pathlib import Path

if __name__ == "__main__":
    files = glob.glob('./config/*.csv')
    files.append('./config/additional_commands')
    grammar_file_path = ('./grammar')
    lst = []
    for file in files:                
        with open(file,'r') as inputFile:
            for item in csv.reader(inputFile):
                if item[0] not in lst:
                    lst.append(item[0])
            
    with open(grammar_file_path,'w') as outputFile:
        for item in lst:
            outputFile.write(item+'\n')
