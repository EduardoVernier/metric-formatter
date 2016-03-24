import csv
from os import listdir
from os.path import isfile, join



header_temp = []
attrib_index = []
output_list = []
list_of_items = []
current_item = []
n_items = 0
n_file = 0

id_dict = {}

my_path = './input/'
csv_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
csv_files.sort()

for filename in csv_files:
    f = open('input/'+filename)
    reader = csv.reader(f)
    item_id = 0
    for item in reader:
        if (n_file == 0 and item[0] == 'Kind'):
            for j in range (1, len(item)):
                header_temp.append(item[j]);

        if (item[0] == 'Public Class' or item[0] == 'Public Abstract Class'):
            if (n_file == 0):
                id_dict[item[1]] = 0
                for j in range (1, len(item)):
                    if (item[j] != ''):
                        current_item.append(item[j])
                        if (n_items == 0):
                            attrib_index.append(j)
                n_items += 1
                list_of_items.append(current_item[:])


            elif (n_file > 0):
                if id_dict.has_key(item[1]):
                    n_items += 1
                    id_dict[item[1]] += 1
                    for j in range (1, len(item)):
                        if (item[j] != ''):
                            current_item.append(item[j])
                            if (n_items == 0):
                                attrib_index.append(j)
                    list_of_items.append(current_item[:])

            current_item = []

    f.close()
    n_file += 1
    output_list.append(list_of_items[:])
    list_of_items = []

# Filter dict to keep only classes that were present in all csv files
# print id_dict
filtered_dict = {k:v for (k,v) in id_dict.items() if v == len(csv_files)-1}
#print set(filtered_dict.items()) ^ set(id_dict.items())

#print output_list


# Write nd file
j = 0
for filename in csv_files:
    header = []
    for i in attrib_index:
        header.append(header_temp[i-1])
    header.remove('Name')
    new_filename = filename.replace("csv", "nd")
    f = open('output/'+ new_filename, "w")
    f.write("DN\n")
    f.write("%d\n" % (len(filtered_dict)))
    f.write("%d\n" % (len(header)))

    for metric in header:
        f.write("%s;" % (metric))

    for item in output_list[j]:
#        print item
        if (item[0] in filtered_dict):
            f.write("\n")
            for attr in item:
                f.write("%s;" % (attr))

    f.close()
    j += 1
