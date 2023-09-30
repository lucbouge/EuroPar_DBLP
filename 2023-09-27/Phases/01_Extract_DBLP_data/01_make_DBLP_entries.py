from Libraries.Config.packages import *
from lxml import etree
import xmltodict as xd
import gc

DBLP_xml_path = Path("Sources", "dblp.xml")

CHUNK_SIZE = 1_000_000


def gc_callback(phase, info):
    print(f"GC {phase} ({memory_size()}): {info}")


# gc.callbacks = [gc_callback]
gc.set_debug(gc.DEBUG_STATS)  # | gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE)
gc.set_threshold(5000000)
print(f"{gc.get_threshold() = }")

################################################################################

# https://lxml.de/api/lxml.etree.iterparse-class.html
# iterparse(self, source, events=("end",), tag=None, attribute_defaults=False, dtd_validation=False, load_dtd=False, no_network=True, remove_blank_text=False, remove_comments=False, remove_pis=False, encoding=None, html=False, recover=None, huge_tree=False, schema=None)
# Incremental parser.
# Parses XML into a tree and generates tuples (event, element) in a SAX-like fashion. event is any of 'start', 'end', 'start-ns', 'end-ns'.


def parse_dblp():
    level = 0
    dblp_entries = list()
    nb_entries = 0
    ##
    context_iterator = etree.iterparse(
        source=DBLP_xml_path,
        events=("start", "end"),
        dtd_validation=True,
        load_dtd=True,
    )
    ##
    print(f"{memory_size() = }")
    ##
    for event, element in context_iterator:
        if event == "start":
            # print(f"{' '*(2*level)} Level {level}: Entering {element.tag} ")
            level += 1
            continue
        ##
        assert event == "end"
        level -= 1
        # print(f"{' '*(2*level)} Level {level}: Exiting {element.tag} ")
        assert level >= 0
        if level == 1:
            entry = make_dblp_entry(element)
            nb_entries += 1
            dblp_entries.append(entry)
            element.clear()
            ##
            if nb_entries % CHUNK_SIZE == 0:
                export_entries(nb_entries, dblp_entries)
                dblp_entries = list()
                print(f"{memory_size() = }")
        elif level == 0:
            assert element.tag == "dblp"
            print("=========== Break")
            export_entries(nb_entries, dblp_entries)
            print(context_iterator.error_log)

        else:
            assert level >= 2


def export_entries(nb_entries, dblp_entries):
    print(f"============ Export: {nb_entries = :_d}, {memory_size() = }")
    dump_data_to_file(dblp_entries, dataname=f"dblp_entries_{nb_entries:010d}")


################################################################################


def make_dblp_entry(element):
    check_type(element, etree.ElementTree)
    entry = xd.parse(etree.tostring(element))
    return entry


def main():
    parse_dblp()
