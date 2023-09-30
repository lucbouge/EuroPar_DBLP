from Libraries.Config.packages import *


def main():
    EuroPar_entries = load_file_to_data(dataname="EuroPar_entries")
    print(f"{len(EuroPar_entries) = }")
    ##
    with open("EuroPar_entries.py", "w") as cout:
        for entry in EuroPar_entries:
            print(entry, file=cout)
    ##
    author_to_year_key_dict = dict()
    for entry in EuroPar_entries:
        assert len(entry) == 1
        item = tuple(entry.items())[0]
        kind = item[0]
        reference = item[1]
        year = reference["year"]
        key = reference["@key"]
        ##
        if kind == "proceedings":
            print(year, reference["title"])
            continue
        ##
        assert kind == "inproceedings", kind
        authors = reference.get("author")
        if authors is None:
            assert reference["@publtype"] == "withdrawn"
            continue
        if not isinstance(authors, list):
            authors = (authors,)
        ##
        for author in authors:
            if isinstance(author, dict):
                author = author["#text"]
            assert isinstance(author, str)
            if author not in author_to_year_key_dict:
                author_to_year_key_dict[author] = list()
            author_to_year_key_dict[author].append((year, key))
        ##
    sorted_authors = tuple(
        (item[0], len(item[1]))
        for item in sorted(
            author_to_year_key_dict.items(), key=lambda item: len(item[1]), reverse=True
        )
    )
    pp.pprint(sorted_authors[:50])
    # print(author_to_year_key_dict["Luc Bougé"])
