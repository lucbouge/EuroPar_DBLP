import xmltodict
import pprint as pp
from gzip import GzipFile
import os
import pickle

dblp_source = "a.xml"
dump_path = "a.pkl"
europar_dump_path = "a_europar.pkl"



count = 0
key_to_entry_dict  = dict() 

def item_callback(path, item):
    global count
    if False: # count > 1_000_000:
        return False
    #
    if count % 1_000 == 0:
        print(f"{count:10,d}", path)
        pp.pprint(item)
        print("="*30)
    assert  path[0][0] == "dblp"
    kind = path[1][0]
    key = path[1][1]["key"]
    assert key not in key_to_entry_dict, key
    key_to_entry_dict[(kind, key)] = (path, item)
    count += 1
    return True



def main1():
    global key_to_entry_dict
    try:
        xmltodict.parse(open(dblp_source, "rb"), item_depth = 2, item_callback=item_callback, disable_entities=False)
    except xmltodict.ParsingInterrupted as e:
        print("Finished")
    with open(dump_path, "wb") as cout:
        print(f"Dumping key_to_entry_dict to {dump_path}")
        pickle.dump(key_to_entry_dict, cout)
        print("Done!")
        for (k, v) in key_to_entry_dict.items():
            print(k)
            print(v)
            print("="*30)



def main2():
    key_europar_to_entry_dict = dict()
    ##
    with open(dump_path, "rb") as cin:
        print(f"Loading key_to_entry_dict from {dump_path}")
        key_to_entry_dict = pickle.load(cin)
        print("Done!")
        for (k, v) in key_to_entry_dict.items():
            (kind, key) = k
            if "europar" in key:
                key_europar_to_entry_dict[k] = v
    with open(europar_dump_path, "wb") as cout:
        print(f"Dumping key_europar_to_entry_dict to {europar_dump_path}")
        pickle.dump(key_europar_to_entry_dict, cout)
        print("Done!")
    

def main3():
    with open(europar_dump_path, "rb") as cin:
        print(f"Loading key_to_entry_dict from {europar_dump_path}")
        key_to_entry_dict = pickle.load(cin)
        print("Done!")
        for (k, v) in key_to_entry_dict.items():
            if "Boug" in repr(k):
                print(k)
                pp.pprint(v)
                print(("="*30))
        print(len(key_to_entry_dict))


main1()