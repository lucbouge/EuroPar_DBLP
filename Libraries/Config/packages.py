import os
import pprint as pp
import re
import csv

import pandas as pd


from typing import Any, Tuple, List, Dict, NamedTuple

from Libraries.Utilities.file import (
    dump_df_to_xlsx,
    load_file_to_data,
    dump_data_to_file,
    make_full_dataname,
    load_xlsx_to_df,
)

from Libraries.Utilities.utilities import *

from bs4 import BeautifulSoup, Tag
from xml.etree.cElementTree import parse

from Libraries.Config.configuration import *
