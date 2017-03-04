import csv
from os import listdir
from os.path import isfile, join

data = []
f = open('./exports.csv')
reader = csv.reader(f)

for item in reader:
	current = []
	for value in item:
		current.append(value)	
	data.append(current)
	
data.pop(0)
for t in range(1, len(data[0]) - 1):
	f = open('output/'+ 'exports.'+ str(t) + '.csv', "w")
	f.write("id,weight\n")			
	for item in data:
		f.write("%s,%f\n" % (item[0], float(item[t])))

	f.close()
