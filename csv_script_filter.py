import sys
import csv
from os import listdir
from os.path import isfile, join

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
                            if (n_items == 0):
                                attrib_index.append(j)
                    n_items += 1
                    current_item.append('0')
                    list_of_items.append(current_item[:])


                elif (cur_file > 0):
                    if id_dict.has_key(item[1]):
                        n_items += 1
                        id_dict[item[1]] += 1
                        for j in range (1, len(item)):
                            if (item[j] != ''):
                                current_item.append(item[j])
                                if (n_items == 0):
                                    attrib_index.append(j)
                        current_item.append('0')
                        list_of_items.append(current_item[:])

                current_item = []

        f.close()
        cur_file += 1
        output_list.append(list_of_items[:])
        list_of_items = []

    return n_files

# Filter dict to keep only classes that were present in all csv files
def filter_items(n_files):
    global id_dict
    return {k:v for (k,v) in id_dict.items() if v == n_files-1}


# Write .data files
def write_items(n_files, filtered_dict, repo_name):
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
        f.write("%d\n" % (len(filtered_dict)))
        f.write("%d\n" % (len(header)))

        for metric in header:
            f.write("%s;" % (metric))

        for item in output_list[j]:
            if (item[0] in filtered_dict):
                f.write("\n")
                for attr in item:
                    f.write("%s;" % (attr))

        f.close()
        j += 1


def main():
    repo_name = sys.argv[1]
    n_files = read_metrics()
    filtered_dict = filter_items(n_files)
    write_items(n_files, filtered_dict, repo_name)

if __name__ == "__main__":
    main()
