import sys
import csv
from os import listdir
from os.path import isfile, join
from statistics import mean
from statistics import stdev


header_temp = []
attrib_index = []
output_list = []
list_of_items = []
id_dict = {}
my_path = './input/'

# Read from /input/ folder
def read_metrics ():
    global list_of_items
    global header_temp
    global attrib_index
    global output_list
    global id_dict
    current_item = []
    n_items = 0
    cur_file = 0

    csv_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    csv_files.sort()
    n_files = len(csv_files)

    for filename in csv_files:
        f = open('input/'+filename)
        reader = csv.reader(f)
        item_id = 0
        for item in reader:
            if (cur_file == 0 and item[0] == 'Kind'):
                for j in range (1, len(item)):
                    header_temp.append(item[j]);

            if (item[0] == 'Public Class' or item[0] == 'Public Abstract Class'):
                if (cur_file == 0):
                    id_dict[item[1]] = 0
                    for j in range (1, len(item)):
                        if (item[j] != ''):
                            current_item.append(item[j])
                            if (n_items == 0): # Fill important attributes list when meets first valid item
                                attrib_index.append(j)
                    n_items += 1
                    current_item = [current_item[0]] + [float(k) for k in current_item[1:]]
                    list_of_items.append(current_item[:])


                elif (cur_file > 0):
                    if item[1] in id_dict:
                        n_items += 1
                        id_dict[item[1]] += 1
                        for j in range (1, len(item)):
                            if (item[j] != ''):
                                current_item.append(item[j])
                        current_item = [current_item[0]] + [float(k) for k in current_item[1:]]
                        list_of_items.append(current_item[:])

                current_item = []

        f.close()
        cur_file += 1
        output_list.append(list_of_items[:])
        list_of_items = []

    return n_files

from itertools import filterfalse
# Filter dict to keep only classes that were present in all csv files
def filter_items(n_files):
    global id_dict
    global output_list
    id_dict = {k:v for (k,v) in id_dict.items() if v == n_files-1}
    output_list = [list(filterfalse(lambda item: item[0] not in id_dict, rev)) for rev in output_list]


def normalize_items():
    global attrib_index
    global output_list

    for attrib in range (1,len(attrib_index)):
        cur_attrib_values = []
        for file_item in output_list:
            for item in file_item:
                cur_attrib_values.append(item[attrib])

        mean_attrib = mean(cur_attrib_values)
        stdev_attrib = stdev(cur_attrib_values)
        if (mean_attrib == 0 or stdev_attrib == 0):
            continue

        # print (mean_attrib, stdev_attrib)
        for file_item in output_list:
            for item in file_item:
                item[attrib] = (item[attrib] - mean_attrib) / stdev_attrib



# Write .data files
def write_items(n_files, repo_name):
    global header_temp
    global attrib_index
    global output_list
    global id_dict

    for j in range(0, n_files):
        header = []
        for i in attrib_index:
            header.append(header_temp[i-1])
        header.remove('Name')
        new_filename = repo_name + "." + str(j) + ".data"
        f = open('output/'+ new_filename, "w")
        f.write("DY\n")
        f.write("%d\n" % (len(id_dict)))
        f.write("%d\n" % (len(header)))

        for metric in header:
            f.write("%s;" % (metric))

        for item in output_list[j]:
            f.write("\n")
            for attr in item:
                f.write("%s;" % (attr))
            f.write("0") ## class info

        f.close()
        j += 1


def main():
    repo_name = sys.argv[1]
    n_files = read_metrics()
    filter_items(n_files)
    normalize_items()
    write_items(n_files, repo_name)

if __name__ == "__main__":
    main()
