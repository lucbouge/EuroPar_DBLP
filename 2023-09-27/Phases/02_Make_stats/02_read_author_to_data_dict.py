from Libraries.Config.packages import *


def main():
    author_to_data_dict = load_file_to_data(dataname="DBLP_author_to_data_dict")
    print(f"{len(author_to_data_dict) = :_d}")
    quit()
    for author, data in author_to_data_dict.items():
        pp.pprint((author, data))
