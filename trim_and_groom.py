import os
import csv
import argparse

g_verbose = False

def main():
    parse_args()
    election_map_dict = extract_election_map()
    prec_map_dict = extract_precinct_map()
    
    # print(election_map_dict)
    # print(prec_map_dict)
    trim(election_map_dict, prec_map_dict)


def trim(election_map_dict, prec_map_dict):
    
    # predefined information
    fve_indexs_of_interest = [6, 7, 8, 11, 151]
    fve_index_of_interest_labels = ['Gender', 'DOB', 'Registration Date', 'Current Party', 'County']
    # some entries must be there (7, 8, 151)
    fve_index_of_interest_null_value = {6:'U', 11:'NON'}
    election_map_offset_index = 70
    in_data_dir = './unmod_data/'
    out_data_dir = './mod_data/'

    for filename in os.listdir(in_data_dir):
        in_path = in_data_dir + filename
        out_path = out_data_dir + filename
        if '_fve_' in filename:
            county_name = filename.split("_")[0]

            district_map_labels = []
            for tup in prec_map_dict[county_name]:
               district_map_labels.append(tup[1])
            district_map_offset_index = 30
            election_map_labels = []
            for tup in election_map_dict[county_name]:
                election_map_labels.append(tup[1] + ' Method')
                election_map_labels.append(tup[1] + ' Party')

            with open(in_path, newline='', encoding='utf8') as csv_in_file, open(out_path, 'w+', newline='', encoding='utf8') as csv_out_file:
                reader = csv.reader(csv_in_file, delimiter='\t')
                writer = csv.writer(csv_out_file, delimiter='\t')
                # add csv header information
                writer.writerow(fve_index_of_interest_labels + district_map_labels + election_map_labels)
                # for every row in the original data set
                for row in reader:
                    fve_data_to_write = []
                    # add the value at the indexes of interest
                    for i in fve_indexs_of_interest:
                        val = row[i] if row[i] != "" else fve_index_of_interest_null_value[i]
                        fve_data_to_write.append(val)
                    # add the value of the precinct
                    for tup in prec_map_dict[county_name]:
                        # entry must be here
                        index = tup[0]
                        val = row[index+district_map_offset_index]
                        fve_data_to_write.append(val)
                    # add the value of the election party and method
                    for tup in election_map_dict[county_name]:
                        index = tup[0]
                        vote_method = row[(index*2) + election_map_offset_index] if row[(index*2) + election_map_offset_index] != "" else 'DNV'
                        vote_party = row[(index*2) + 1 + election_map_offset_index] if row[(index*2) + 1 + election_map_offset_index] != "" else 'DNV'
                        fve_data_to_write.append(vote_method)
                        fve_data_to_write.append(vote_party)
                    writer.writerow(fve_data_to_write)
                csv_in_file.close()
                csv_out_file.close()

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
                        election_map_dict[county_name].append((to_zero_start(int(row[1])), row[2]))
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
                        prec_map_dict[county_name].append((to_zero_start(int(row[1])), row[3]))
                        v_print(row[1])
                csvfile.close()
    v_print(prec_map_dict)
    return prec_map_dict


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
    parser = argparse.ArgumentParser(description="Groom data set")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enables verbose printing.')
    args = parser.parse_args()
    if args.verbose:
        global g_verbose
        g_verbose = True

if __name__ == "__main__":
    main()