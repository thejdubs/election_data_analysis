import os
import csv
import argparse
import mysql.connector
import copy
from datetime import datetime

g_verbose = False

def main():
    parse_args()
    con = connect()
    cursor = con.cursor()

    county_of_interest = ['beaver', 'centre', 'fayette', 'monroe', 'schuylkill']

    votes_dict = parse_results(county_of_interest)
    party_dict = sql_party(county_of_interest, cursor)
    
    print(votes_dict)
    print(party_dict)

    unloyal_ratio_dict = calc_unloyal_ratio(votes_dict, party_dict)

    print(unloyal_ratio_dict)

    loyalty_dict = find_loyalities(unloyal_ratio_dict)

    pretty_print(loyalty_dict)

    trimmed = trim(loyalty_dict)

    print(trimmed)
    
    cursor.close()
    con.close()


def connect():
    con = mysql.connector.connect(host='localhost', user='root', passwd='greatwhite2', db='election')
    return con
    
def parse_results(county_of_interest):
    votes_dict = {'centre':[], 'beaver':[], 'fayette':[], 'monroe':[], 'schuylkill':[]}

    data_dir = './'
    path = data_dir + '2016_results.csv'
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row[0].lower() in county_of_interest:
                votes_dict[row[0].lower()].extend((int(row[1].replace(',','')), int(row[2].replace(',','')), sum([int(i.replace(',','')) for i in row[3:]])))
        csvfile.close()
    
    return votes_dict

def sql_party(county_of_interest, cursor):
    party_dict = {'centre':[], 'beaver':[], 'fayette':[], 'monroe':[], 'schuylkill':[]}
    for county in county_of_interest:
        exec_string = "SELECT count(2016_GENERAL_ELECTION_Party) as count FROM " + county + " where 2016_GENERAL_ELECTION_Party = 'D';"
        cursor.execute(exec_string)
        count = cursor.fetchall()[0][0]
        party_dict[county].append(count)
        exec_string = "SELECT count(2016_GENERAL_ELECTION_Party) as count FROM " + county + " where 2016_GENERAL_ELECTION_Party = 'R';"
        cursor.execute(exec_string)
        count = cursor.fetchall()[0][0]
        party_dict[county].append(count)
        exec_string = "SELECT count(2016_GENERAL_ELECTION_Party) as count FROM " + county
        exec_string += " where 2016_GENERAL_ELECTION_Party != 'R' and 2016_GENERAL_ELECTION_Party != 'D' and 2016_GENERAL_ELECTION_Party != 'DNV';"
        cursor.execute(exec_string)
        count = cursor.fetchall()[0][0]
        party_dict[county].append(count)
    return party_dict

def calc_unloyal_ratio(votes_dict, party_dict):
    unloyal_ratio_dict = copy.deepcopy(votes_dict)
    for key in votes_dict:
        unloyal_ratio_dict[key].clear()
        for i in range(len(votes_dict[key])):
            unloyal_ratio_dict[key].append(votes_dict[key][i]/party_dict[key][i])
    return unloyal_ratio_dict

def find_loyalities(unloyal_ratio_dict):
    p_breakdown = { 'dem': [], 'rep': [], 'oth': [] }
    loyalty_dict = { 'dem': [[],[]], 'rep': [[],[]], 'oth': [[],[]] }

    for key in unloyal_ratio_dict:
        p_breakdown['dem'].append((key, unloyal_ratio_dict[key][0]))
        p_breakdown['rep'].append((key, unloyal_ratio_dict[key][1]))
        p_breakdown['oth'].append((key, unloyal_ratio_dict[key][2]))
    
    for key in p_breakdown:
        max = 0
        min = 10
        for tup in p_breakdown[key]:
            if tup[1] < min:
                min = tup[1]
                loyalty_dict[key][0] = tup
            if tup[1] > max:
                max = tup[1]
                loyalty_dict[key][1] = tup
                
    return loyalty_dict

def pretty_print(loyalty_dict):
    short_to_long = {'dem': 'Democrat', 'rep': 'Republican', 'oth':'No Affiliation'}
    for key in loyalty_dict:
        print("For the " + short_to_long[key] + " party, loyalties are:")
        print("Least Loyal: " + loyalty_dict[key][0][0] + " with a score of " + str(loyalty_dict[key][0][1])[:5] + ".")
        print("Most Loyal: " + loyalty_dict[key][1][0] + " with a score of " + str(loyalty_dict[key][1][1])[:5] + ".\n")

def trim(loyalty_dict):
    compact = {'dem': [], 'rep': [], 'oth': [] }
    for key in loyalty_dict:
        compact[key].append(loyalty_dict[key][0][0])
        compact[key].append(loyalty_dict[key][1][0])
    
    return compact

def parse_args():
    parser = argparse.ArgumentParser(description="Groom data set")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enables verbose printing.')
    args = parser.parse_args()
    if args.verbose:
        global g_verbose
        g_verbose = True


# verbose printing
def v_print(msg):
    global g_verbose
    if g_verbose:
        print(msg)

if __name__ == "__main__":
    main()