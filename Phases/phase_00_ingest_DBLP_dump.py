from Libraries.Config.packages import *

import gzip
from html.parser import HTMLParser
from html.entities import name2codepoint
import xmltodict


def main():
    dblp_entries = make_dblp_entries()
    dump_data_to_file(dblp_entries, dataname="dblp_entries")
    print(f"{len(dblp_entries)=}")


################################################################################


class MyHTMLParser(HTMLParser):
    def __init__(self, *, callback=None):
        super().__init__()
        self.depth = 0
        self.xml = ""
        assert callback is not None
        self.callback = callback

    def handle_starttag(self, tag, attrs):
        text = self.get_starttag_text()
        assert text is not None
        if self.depth > 0:
            self.xml += text
        self.depth += 1

    def handle_endtag(self, tag):
        self.depth -= 1
        self.xml += f"</{tag}>"
        assert self.depth >= 0
        if self.depth == 1:
            self.callback(self.xml)
            self.xml = ""

    def handle_data(self, data):
        if self.depth > 0:
            self.xml += data

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)
        self.xml += c
        print(self.xml)
        quit()

    def handle_charref(self, name):
        if name.startswith("x"):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)
        self.xml += c

    def handle_decl(self, data):
        print("Decl     :", data)


################################################################################

count = 0
dblp_entries = list()


def callback(entry):
    dblp_entries.append(entry)


def make_dblp_entries():
    # with open("a.xml", "rb") as cin:
    with gzip.open(DBLP_DUMP_ORIGINAL_FILENAME) as cin:
        parser = MyHTMLParser(callback=callback)
        for (i, line) in enumerate(cin):
            if i % 1_000_000 == 0:
                print(f"{i:15,d}")
            parser.feed(line.decode())
    return dblp_entries
