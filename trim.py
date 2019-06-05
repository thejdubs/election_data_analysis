import os
import csv
import argparse

g_verbose = False

def main():
    election_map_dict = extract_election_map()
    prec_map_dict = extract_precinct_map()

    trim(election_map_dict, prec_map_dict)

    # print(election_map_dict)
    # print(prec_map_dict)

def trim(election_map_dict, prec_map_dict):
    fve_indexs_of_interest = [6, 7, 8, 11]
    district_map_offset_index = 30
    election_map_offset_index = 70
    in_data_dir = './unmod_data/'
    out_data_dir = './mod_data/'
    for filename in os.listdir(in_data_dir):
        in_path = in_data_dir + filename
        out_path = out_data_dir + filename
        if '_fve_' in filename:
            county_name = filename.split("_")[0]
            with open(in_path, newline='', encoding='utf8') as csv_in_file, open(out_path, 'w+', newline='', encoding='utf8') as csv_out_file:
                reader = csv.reader(csv_in_file, delimiter='\t')
                writer = csv.writer(csv_out_file, delimiter='\t')
                # for every row in the original data set
                for row in reader:
                    fve_data_to_write = []
                    # add the value at the indexes of interest
                    for i in fve_indexs_of_interest:
                        fve_data_to_write.append(row[i])
                    # add the value of the precinct
                    for i in prec_map_dict[county_name]:
                        fve_data_to_write.append(row[i+district_map_offset_index])
                    # add the value of the election party and method
                    for i in election_map_dict[county_name]:
                        fve_data_to_write.append(row[(i*2) + election_map_offset_index])
                        fve_data_to_write.append(row[(i*2) + 1 + election_map_offset_index])
                    writer.writerow(fve_data_to_write)
                csv_in_file.close()
                csv_out_file.close()
    

def parse_args():
    parser = argparse.ArgumentParser(description="Groom data set")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enables verbose printing.')
    args = parser.parse_args()
    if args.verbose:
        global g_verbose
        g_verbose = True


def extract_election_map():
    # county files to look at
    election_map_dict = {'centre':[], 'beaver':[], 'fayette':[], 'monroe':[], 'schuylkill':[]}

    data_dir = './unmod_data/'
    for filename in os.listdir(data_dir):
        path = data_dir + filename
        if 'election_map' in filename:
            county_name = filename.split("_")[0]
            v_print(county_name)
            with open(path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')
                for row in reader:
                    if any(s in row for s in(
                        '2014 GENERAL PRIMARY', '2014 GENERAL ELECTION',
                        '2016 GENERAL PRIMARY', '2016 GENERAL ELECTION',
                        '2018 GENERAL PRIMARY', '2018 GENERAL ELECTION')
                    ):
                        election_map_dict[county_name].append(to_zero_start(int(row[1])))
                        v_print(row[1])
                csvfile.close()
    v_print(election_map_dict)
    return election_map_dict

def extract_precinct_map():
    # county files to look at
    prec_map_dict = {'centre':[], 'beaver':[], 'fayette':[], 'monroe':[], 'schuylkill':[]}

    data_dir = './unmod_data/'
    for filename in os.listdir(data_dir):
        path = data_dir + filename
        if 'zone_types' in filename:
            county_name = filename.split("_")[0]
            v_print(county_name)
            with open(path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')
                for row in reader:
                    if "Precinct" == row[3]:
                        prec_map_dict[county_name].append(to_zero_start(int(row[1])))
                        v_print(row[1])
                csvfile.close()
    v_print(prec_map_dict)
    return prec_map_dict


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

if __name__ == "__main__":
    main()