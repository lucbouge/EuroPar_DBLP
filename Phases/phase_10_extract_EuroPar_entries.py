from Libraries.Config.packages import *

key_pattern = re.compile(r"conf/europar/([\d\w-]+)")
assert key_pattern is not None

def main():
    dblp_entries = load_file_to_data(dataname="dblp_entries")
    print(f"{len(dblp_entries)=:,d}")
    ##
    europar_authors = make_europar_authors(dblp_entries=dblp_entries)
    print(f"{len(europar_authors)=:,d}")
    ##
    author_to_entries_dict = make_author_to_entries_dict(dblp_entries=dblp_entries, europar_authors=europar_authors)
    dump_data_to_file(author_to_entries_dict, dataname="author_to_entries_dict")
    print(f"{len(author_to_entries_dict)=:,d}")


################################################################################

def make_author_to_entries_dict(*, dblp_entries=None, europar_authors=None):
    assert dblp_entries is not None
    assert europar_authors is not None
    ##
    author_to_entries_dict = dict()
    for (i, entry) in enumerate(dblp_entries):
        if i%100_000 == 0:
            print(f"{i:10,d}")
        soup = BeautifulSoup(entry, features="xml")
        for author_tag in soup.find_all("author"):
            author = author_tag.get_text()
            if author in europar_authors:
                if author not in author_to_entries_dict:
                    author_to_entries_dict[author] = list()
                author_to_entries_dict[author].append(entry)
    return author_to_entries_dict
   
################################################################################

def make_europar_authors(*,dblp_entries=None):
    assert dblp_entries is not None
    ##
    europar_authors= set()
    for entry in dblp_entries:
        if "europar" not in entry.lower():
            continue
        ##
        soup = BeautifulSoup(entry, features="xml")
        root = soup.find()
        assert isinstance(root, Tag)
        assert "key" in root.attrs
        key = root["key"]
        assert isinstance(key, str), key
        ##
        m  = re.fullmatch(key_pattern, key)
        if m is None:
            # print_error(f"Bad key {key}")
            continue
        ##
        for author_tag in root.find_all("author"):
            author = author_tag.get_text()
            europar_authors.add(author)
    return europar_authors
   
        

        
    

