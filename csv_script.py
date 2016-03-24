import csv
from os import listdir
from os.path import isfile, join

header_temp = []
attrib_index = []
list_of_items = []
current_item = []
n_items = 0

my_path = './input/'
csv_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
csv_files.sort()


for filename in csv_files:
    f = open('input/'+filename)
    reader = csv.reader(f)
    item_id = 0
    for item in reader:
        if (item[0] == 'Kind'):
            for j in range (1, len(item)):
                header_temp.append(item[j]);

        if (item[0] == 'Public Class' or item[0] == 'Public Abstract Class'):
            for j in range (1, len(item)):
                if (item[j] != ''):
                    current_item.append(item[j])
                    if (n_items == 0):
                        attrib_index.append(j)
            list_of_items.append(current_item[:])
            current_item = []
            n_items += 1

    f.close()


    # Write nd file
    header = []
    for i in attrib_index:
        header.append(header_temp[i-1])
    header.remove('Name')
    new_filename = filename.replace("csv", "nd")
    f = open('output/'+ new_filename, "w")
    f.write("DN\n")
    f.write("%d\n" % (n_items))
    f.write("%d\n" % (len(header)))

    for metric in header:
        f.write("%s;" % (metric))

    for item in list_of_items:
        f.write("\n")
        for attr in item:
            f.write("%s;" % (attr))

    f.close()
