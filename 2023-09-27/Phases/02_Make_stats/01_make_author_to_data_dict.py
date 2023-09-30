from Libraries.Config.packages import *

DBLP_entries_pattern = "dblp_entries_[0-9]*[0-9].pkl"

# <!ELEMENT dblp (article|inproceedings|proceedings|book|incollection|phdthesis|mastersthesis|www|person|data)*>


def main():
    DBLP_entries_files = Path("PKL").glob(DBLP_entries_pattern)
    ##
    author_to_data_dict = dict()
    for DBLP_entries_file in DBLP_entries_files:
        assert isinstance(DBLP_entries_file, Path)
        print(f"=============== {DBLP_entries_file}")
        dataname = str(DBLP_entries_file.stem)
        DBLP_entries = load_file_to_data(dataname=dataname)
        ##
        new_author_to_data_dict = make_author_to_data_dict(DBLP_entries=DBLP_entries)
        ##
        for author, data in new_author_to_data_dict.items():
            if author not in author_to_data_dict:
                author_to_data_dict[author] = list()
            author_to_data_dict[author] += new_author_to_data_dict[author]
        ##
    dump_data_to_file(author_to_data_dict, dataname="DBLP_author_to_data_dict")


# <!ELEMENT dblp (article|inproceedings|proceedings|book|incollection|phdthesis|mastersthesis|www|person|data)*>


kinds = {"inproceedings", "article", "book", "incollection"}


def make_author_to_data_dict(*, DBLP_entries):
    author_to_data_dict = dict()
    for entry in DBLP_entries:
        assert len(entry) == 1
        item = tuple(entry.items())[0]
        kind = item[0]
        if kind not in kinds:
            continue
        reference = item[1]
        key = reference["@key"]
        year = reference.get("year")
        if year is None:
            continue
        ##
        authors = reference.get("author")
        if authors is None:
            continue
        if not isinstance(authors, (list, tuple, set)):
            authors = (authors,)
        ##
        for author in authors:
            if isinstance(author, dict):
                author = author["#text"]
            assert isinstance(author, str)
            if author not in author_to_data_dict:
                author_to_data_dict[author] = list()
            author_to_data_dict[author].append((year, key))
    return author_to_data_dict
