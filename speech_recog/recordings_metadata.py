import os
words = os.listdir("./recordings/")
output = open("./recordings/metadata.csv","w")
for word in words:
    count = len(os.listdir("./recordings/"+word+"/"))
    output.write(word+","+str(count)+"\n")