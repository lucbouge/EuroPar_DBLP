import sys
import re
import pprint as pp
import datetime
from pandas import isna, notna


def get_date_string():
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    return date


###########################################################


def unused(s):
    assert s is not None


###########################################################


ascii_pattern = r"[a-zA-Z0-9_.-]+"


def check_ascii(c):
    assert re.fullmatch(ascii_pattern, c), c


###########################################################


def return_double_items(lst):
    doubles = set()
    elements = set()
    for x in lst:
        if x not in elements:
            elements.add(x)
            continue
        doubles.add(x)
    return doubles


def check_no_double_item(lst):
    doubles = return_double_items(lst)
    return len(doubles) == 0


###########################################################


def eprint(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print("--> ", *args, **kwargs)


def epprint(*args, **kwargs):
    kwargs["stream"] = sys.stderr
    if len(args) > 1:  # Trick for allow for more than one argument!
        args = (args,)
    pp.pprint(args, **kwargs)


def new_chapter(s):
    message = f"""

{'=' * 30} {s}
"""
    print(message)


def new_phase(*, phase=None, modulename=None):
    message = f"""

{'=' * 60} Phase: {phase}, module: {modulename}

"""
    print(message)


def new_section(s):
    message = f"""
{'=' * 15} {s}"""
    print(message)


###########################################################


def print_error(e):
    message = f"""
{'_'*20}
==> Error: {e}
{'_'*20}
"""
    print(message.strip())
