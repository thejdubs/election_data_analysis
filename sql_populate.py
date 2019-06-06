import os
import csv
import argparse
import mysql.connector
from datetime import datetime

g_verbose = False

def main():
    parse_args()
    con = connect()
    cursor = con.cursor()
    generate(cursor)
    con.commit()
    cursor.close()
    con.close()


def connect():
    con = mysql.connector.connect(host='localhost', user='root', passwd='greatwhite2', db='election')
    return con
    
def generate(cursor):
    data_dir = './mod_data/'
    for filename in os.listdir(data_dir):
        if 'schuylkill' in filename:
            path = data_dir + filename
            county_name = filename.split("_")[0]
            with open(path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')
                headers = next(reader)
                create_table(county_name, headers, cursor)
                for row in reader:
                    insert_element(row, county_name, headers, cursor)
                csvfile.close()

def create_table(name, headers, cursor):
    exec_string = ""
    exec_string += "CREATE TABLE IF NOT EXISTS " + name + " (\n"
    # unique id
    exec_string += "id INT AUTO_INCREMENT,\n"
    # gender
    exec_string += headers[0] + " VARCHAR(3) NOT NULL,\n"
    # dob and reg date
    for date in headers[1:3]:
        exec_string += date.replace(' ', '_') + " DATE NOT NULL,\n"
    # current party
    exec_string += headers[3].replace(' ', '_') + " VARCHAR(10) NOT NULL,\n"
    # county
    exec_string += headers[4] + " VARCHAR(50) NOT NULL,\n"
    # precinct and elections
    for val in headers[5:]:
        exec_string += val.replace(' ', '_') + " VARCHAR(10) NOT NULL,\n"
    # P_key and end
    exec_string += "PRIMARY KEY (id)\n);"

    # print(exec_string)
    cursor.execute(exec_string)

def insert_element(row, name, headers, cursor):
    # convert date string to proper datetime for insertion
    row[1] = datetime.strptime(row[1], '%m/%d/%Y').strftime('%Y-%m-%d')
    row[2] = datetime.strptime(row[2], '%m/%d/%Y').strftime('%Y-%m-%d')

    exec_string = ""
    exec_string += "INSERT INTO " + name + " ("
    for col_name in headers:
        exec_string += col_name.replace(' ', '_') + ", "
    # remove last comma
    exec_string = exec_string[:-2]
    exec_string += ") VALUES ("
    for val in row:
        exec_string += "\'" + val + "\'" + ", "
    # remove last comma and add ender
    exec_string = exec_string[:-2] + ");"

    v_print(exec_string)
    cursor.execute(exec_string)


    
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