import re
import subprocess
import csv
import os
corpus = list(csv.reader(open("./vaac_core/vaac_core_corpus","r")))

files = os.listdir("./vaac_core/recordings/")
files.sort()



for f in files:
    lis = re.findall(r'\d+', f)     
    if len(lis) == 2:
        n = lis[0]
        i = lis[1]
        dirname = "./recordings/"+corpus[int(n)][0]
        dirname = dirname.lower()
        fname = "./vaac_core/recordings/word"+n+"_"+i+".wav"        
        os.system("mkdir"+" -p "+dirname)
        os.system("cp "+fname+" "+dirname )

        
        
