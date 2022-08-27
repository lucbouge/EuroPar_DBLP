from Libraries.Config.packages import *


def sorting_function(item):
    (name, entries) = item
    return (len(entries), name)


################################################################################


def main():
    author_to_entries_dict = load_file_to_data(dataname="author_to_entries_dict")
    author_to_selected_entries_dict = dict(
        (author, select_entries(entries=entries, author=author))
        for (author, entries) in author_to_entries_dict.items()
    )
    dump_data_to_file(
        author_to_selected_entries_dict, dataname="author_to_selected_entries_dict"
    )
    #
    for (author, entries) in sorted(
        author_to_selected_entries_dict.items(), key=sorting_function, reverse=True
    ):
        nb_entries = len(entries)
        nb_europar_entries = len(tuple(entry for entry in entries if entry.is_europar))
        print(
            author,
            nb_entries,
            nb_europar_entries,
        )


################################################################################

key_pattern = re.compile(r"\w+")


class Entry(NamedTuple):
    key: str
    year: int
    author: str
    is_europar: bool
    kind: str
    entry: str


def select_entries(*, entries=None, author=None) -> List[Entry]:
    assert entries is not None
    assert author is not None
    ##
    filtered_entries = list()
    for entry in entries:
        soup = BeautifulSoup(entry, features="xml")
        root_tag = soup.find()
        assert isinstance(root_tag, Tag)
        ##
        key = root_tag["key"]
        assert isinstance(key, str)
        key_parts = key.split("/")
        assert len(key_parts) >= 2, key_parts
        assert re.fullmatch(key_pattern, key_parts[0])
        ##
        kind = root_tag.name
        assert kind in DBLP_CATEGORIES, kind
        if kind not in {"inproceedings", "incollection", "article", "book"}:
            continue
        ##
        year_tag = root_tag.find("year")
        if year_tag is None:
            # print_error(f"Empty year for {root_tag}")
            continue
        year = int(year_tag.get_text())
        assert 1900 <= year <= 2030, year
        ##
        is_europar = key_parts[1] == "europar"
        ##
        new_entry = Entry(
            key=key,
            year=year,
            is_europar=is_europar,
            kind=kind,
            author=author,
            entry=entry,
        )
        filtered_entries.append(new_entry)
    return filtered_entries
