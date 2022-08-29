from Libraries.Config.packages import *

import gzip
from lxml import etree, objectify
import xmltodict

# https://lxml.de/parsing.html

source = "Sources/test.xml"

entries = list()


def main():
    root = get_root(source)
    ##
    print("="*100)
    dblp_entries = dict()
    for (i, entry) in enumerate(root.iterchildren()):
        assert entry.tag in DBLP_CATEGORIES, entry.tag
        assert "key" in entry.keys()
        key = entry.get("key")
        assert key not in dblp_entries, key
        if i % 1_000_000 == 0:
            print(f"{i:15,d}", key)
        dblp_entries[key] = xmltodict.parse(etree.tostring(entry))
    dump_data_to_file(dblp_entries, dataname="dblp_entries")


def get_root(source):
    parser = etree.XMLPullParser(
        # events=("end"),
        attribute_defaults=True,
        dtd_validation=True,
    )
    # with open(source, "rb") as cin:
    with gzip.open(DBLP_DUMP_ORIGINAL_FILENAME) as cin:
        ##
        prelude(cin, parser)
        ##
        for (i, line) in enumerate(cin):
            if i % 1_000_000 == 0:
                print(f"{i:15,d}")
            parser.feed(line)
        ##
    root = parser.close()
    print(root, type(root))
    return root


def prelude(cin, parser):
    line = next(cin)
    assert line == b'<?xml version="1.0" encoding="ISO-8859-1"?>\n', line
    line = b'<?xml version="1.0"?>\n'
    parser.feed(line)
    ##
    line = next(cin)
    assert line == b'<!DOCTYPE dblp SYSTEM "dblp.dtd">\n', line
    line = b'<!DOCTYPE dblp SYSTEM "Sources/dblp.dtd">\n'
    parser.feed(line)
