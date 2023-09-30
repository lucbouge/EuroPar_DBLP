from Libraries.Config.packages import *

key_pattern = re.compile(r"conf/europar/", flags=re.IGNORECASE)

DBLP_entries_pattern = "dblp_entries_[0-9]*[0-9].pkl"


def main():
    DBLP_entries_files = Path("PKL").glob(DBLP_entries_pattern)
    ##
    EuroPar_entries = list()
    for DBLP_entries_file in DBLP_entries_files:
        assert isinstance(DBLP_entries_file, Path)
        print(f"=============== {DBLP_entries_file}: {len(EuroPar_entries)}")
        new_EuroPar_entries = extract_EuroPar_entries(DBLP_entries_file)
        EuroPar_entries += new_EuroPar_entries
    dump_data_to_file(EuroPar_entries, dataname="EuroPar_entries")


def extract_EuroPar_entries(DBLP_entries_file: Path) -> List[dict]:
    assert isinstance(DBLP_entries_file, Path), DBLP_entries_file
    dataname = str(DBLP_entries_file.stem)
    DBLP_entries = load_file_to_data(dataname=dataname)
    ##
    new_EuroPar_entries = list()
    for entry in DBLP_entries:
        if is_EuroPar(entry):
            new_EuroPar_entries.append(entry)
    return new_EuroPar_entries


def is_EuroPar(entry) -> bool:
    assert isinstance(entry, dict), entry
    assert len(entry) == 1, entry
    item = tuple(entry.items())[0]
    kind = item[0]
    reference = item[1]
    ##
    key = reference["@key"]
    # print(key)
    return re.match(key_pattern, key) is not None
