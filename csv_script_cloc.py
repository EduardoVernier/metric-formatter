import csv
from os import listdir
from os.path import isfile, join

my_path = './input/'
csv_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
csv_files.sort(key=len)


for filename in csv_files:
    ids = []
    loc = []
    f = open('input/'+filename)
    reader = csv.reader(f)
    
    i = 0
    for item in reader:
        if (item[0] != 'language'):
            ids.append(item[1][2:])
            loc.append(int(item[2])+int(item[3])+int(item[4]))
    f.close()

    f = open('output/'+ 'calcuta.'+ filename, "w")
    f.write("id,weight\n")
        
    for j in range(0, len(ids)):
        f.write("%s,%d\n" % (ids[j], loc[j]))
        
    f.close()
    i += 1
