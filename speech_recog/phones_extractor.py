import argparse
desc='''This script extracts phones from the dictionary file and puts them in the .phone file.'''
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("--modeldir",required=True,type=str, help="Takes path to model directory.")

args = parser.parse_args()
model_dir_string = args.modeldir


inputfile = open(model_dir_string+"/"+model_dir_string+"_lm/"+model_dir_string+".dic","r")
outputfile = open(model_dir_string+"/"+model_dir_string+"_lm/"+model_dir_string+".phone","w")
phones = ['SIL']
for line in inputfile:
	for item in line.split()[1:]:
		if item not in phones:
			phones.append(item)
phones.sort()

for phone in phones:
	outputfile.write(phone+"\n")
