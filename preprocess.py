import csv
app_names = [
            'code', 'firefox', 'gedit',
            'general', 'nautilus', 'gnome-terminal',
        ]

keysymfilepath = './config/keys.csv'
with open(keysymfilepath,'r') as keysymfile:
    keysym = [item[1] for item in list(csv.reader(keysymfile))]

for app_name in app_names:
    sourcepath = f'./config/{app_name}.csv'
    destpath = f'./data/keys/{app_name}.csv'    
    lst = []

    with open(sourcepath, 'r') as sourcefile:
        lst = list(csv.reader(sourcefile))

        for idx,line in enumerate(lst):
            if not all(c.isalpha() or c.isspace() for c in line[0]):
                print('Error: Found invalid character in command, line',idx+1,'of file:',sourcepath,"\n\t",line)
            key_string = line[1].split() #to account for spaces
            for item in key_string:
                shortcuts = item.split('+')
                for key in shortcuts:
                    if key not in keysym:
                        print('Error: Found invalid keysym:',key,'in line:',idx+1,'of file:',sourcepath,"\n\t",line)
                        
        for item in lst:
            item[0] = item[0].strip()
            item[1] = item[1].strip()
            item[0] = ' '.join(sorted(item[0].split()))
            item[0] = item[0].upper()
        
        lst = sorted(lst,key=lambda x: x[0])

    with open(destpath,'w') as destfile:
        for item in lst:
            destfile.write(item[0]+','+item[1]+"\n")

    with open(sourcepath,'r') as sourcefile:
        lst = list(csv.reader(sourcefile))
        for item in lst:
            item[0] = item[0].strip()
            item[1] = item[1].strip()
            item[0] = ' '.join(sorted(item[0].split()))
            item[0] = item[0].lower()
        lst = sorted(lst,key=lambda x: x[0])

    with open(sourcepath,'w') as destfile:
        for item in lst:
            destfile.write(item[0]+','+item[1]+"\n")
