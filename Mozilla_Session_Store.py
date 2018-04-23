import lz4.block as lz4
import sys
import json
import argparse

class MozLz4aError(Exception):
    pass

class InvalidHeader(MozLz4aError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def decompress(file_obj):
    if file_obj.read(8) != b"mozLz40\0":
        raise InvalidHeader("Invalid magic number")
    return lz4.decompress(file_obj.read())

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Write Mozilla Session Tabs")
    argparser.add_argument(
            "out_file",
            help="Path to output file."
        )

    parsed_args = argparser.parse_args()

    in_file_path = "C:\\Users\\SASMIT_DAS\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\82145q4w.default-1519968907351\\sessionstore-backups\\recovery.jsonlz4"
    try:
        in_file = open(in_file_path, "rb")
    except IOError as e:
        print("Could not open input file `%s' for reading: %s" % (parsed_args.in_file, e), file=sys.stderr)
        sys.exit(2)
    
    # try:
    #     out_file = open(parsed_args.out_file, "wb")
    # except IOError as e:
    #     print("Could not open output file `%s' for writing: %s" % (parsed_args.out_file, e), file=sys.stderr)
    #     sys.exit(3)

    try:
        data = decompress(in_file)
    except Exception as e:
        print("Could not compress/decompress file `%s': %s" % (parsed_args.in_file, e), file=sys.stderr)
        sys.exit(4)

    data_json = json.loads(data)
    pretty_json = json.dumps(data_json,indent=4,sort_keys=True)
    with open('pretty_json_'+parsed_args.out_file+'.json','w') as f1:
    	f1.write(pretty_json)

    window_details = data_json["windows"]
    wcount = 0
    for window in window_details:
    	try:
    		fname = parsed_args.out_file+'_'+str(wcount)+'.csv'
    		wcount += 1
    		out_file = open("C:\\Users\\SASMIT_DAS\\Desktop\\SessionStore\\"+fname, 'w')
    	except IOError as e:
    		print("Could not open output file `%s' for writing: %s" % (parsed_args.out_file, e), file=sys.stderr)
    		sys.exit(3)
    	tabs = window["tabs"]
    	for item in tabs:
    		entries = item['entries']
    		for entry in entries:
    			if "originalURI" in entry.keys():
    				out_file.write("'"+str(entry['title']).replace(',',' ')+"'"+','+entry['originalURI']+'\n')

    		#out_file.write(item["entries"][1]["title"]+','+item["entries"][1]["originalURI"]+'\n')
    	out_file.close()


    # try:
    #     out_file.write(data)
    # except IOError as e:
    #     print("Could not write to output file `%s': %s" % (parsed_args.out_file, e), file=sys.stderr)
    #     sys.exit(5)
    # finally:
    #     out_file.close()


