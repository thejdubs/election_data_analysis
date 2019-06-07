import os
import csv
import argparse
from datetime import date, datetime

g_verbose = False

def main():
    parse_args()
    group()
    #nom_to_bin()

def group():
    
    in_data_dir = './csv_data/'
    out_data_dir = './csv_data/grouped/'

    for filename in os.listdir(in_data_dir):
        in_path = in_data_dir + filename
        out_path = out_data_dir + "grouped_" + filename
        if '.csv' in filename:
            with open(in_path, newline='', encoding='utf8') as csv_in_file, open(out_path, 'w+', newline='', encoding='utf8') as csv_out_file:
                reader = csv.reader(csv_in_file)
                writer = csv.writer(csv_out_file, quoting=csv.QUOTE_ALL)
                headers = next(reader)
                newheaders = []
                newheaders.extend(headers[0:6])
                newheaders.extend(headers[7::2])
                newheaders.extend(headers[6::2])
                writer.writerow(newheaders)
                for row in reader:
                    data_to_write = []
                    data_to_write.append(row[0])
                    data_to_write.append(group_dob(row[1]))
                    data_to_write.append(group_reg_date(row[2]))
                    data_to_write.append(group_party(row[3]))
                    data_to_write.extend(row[4:6])
                    data_to_write.extend(group_party(row[7::2]))
                    data_to_write.extend(row[6::2])
                    writer.writerow(data_to_write)

                csv_in_file.close()
                csv_out_file.close()

def group_dob(val):
    val = datetime.strptime(val, '%m/%d/%Y')
    group = [('Y', 25), ('YA', 40), ('MA', 60), ('RA', 75), ('E', 200)]
    age = calculate_age(val)
    for tup in group:
        if age <= tup[1]:
            return tup[0]

def group_reg_date(val):
    val = datetime.strptime(val, '%m/%d/%Y')
    group = [('S', 1), ('1E', 4), ('2E', 8), ('6E', 24), ('UE', 200)]
    age = calculate_age(val)
    for tup in group:
        if age <= tup[1]:
            return tup[0]

def group_party(lst):
    r_lst = []
    if isinstance(lst, list):
        for p in lst:
            if p != 'R' and p != 'D' and p != 'DNV':
                r_lst.append('OTH')
            else:
                r_lst.append(p)
    else:
        if lst != 'R' and lst != 'D' and lst != 'DNV':
            return 'OTH'
        else:
            return lst
    return r_lst

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


# verbose printing
def v_print(msg):
    global g_verbose
    if g_verbose:
        print(msg)

# makes 1 based indexes into 0 based
def to_zero_start(val):
    return val - 1

# makes 0 based indexes into 1 based
def to_one_start(val):
    return val + 1


def parse_args():
    parser = argparse.ArgumentParser(description="Transform nominals to numerics data set")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enables verbose printing.')
    args = parser.parse_args()
    if args.verbose:
        global g_verbose
        g_verbose = True

if __name__ == "__main__":
    main()