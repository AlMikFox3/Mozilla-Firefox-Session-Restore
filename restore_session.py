import os
import csv
import argparse

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="starts with filename")
    argparser.add_argument(
            "starts_file",
            help="How does the file you are looking for start with."
        )
    parsed_args = argparser.parse_args()
    directory = "C:\\Users\\SASMIT_DAS\\Desktop\\SessionStore"
    file_list = []
    for file in os.listdir(directory):
    	if file.startswith(parsed_args.starts_file):
    		file_list.append(file)

    for f in file_list:
    	fobj = open(f,'r')
    	csv_obj = csv.reader(fobj, delimiter = ',')
    	string = "start firefox"
    	for row in csv_obj:
    		string = string + " " + str(row[1])
    		print (row)
    	os.system(string)
