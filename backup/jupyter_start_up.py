%load_ext autoreload
%autoreload 2
%matplotlib inline
%precision 4
%reload_ext autoreload

import re
import sys
import math
import random
import os
from datetime import datetime


import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


import numpy as np
from matplotlib import pyplot as plt


import warnings
warnings.filterwarnings(action='once')
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import pandas as pd
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None)
pd.options.display.max_rows = None

import seaborn as sns
sns.set(style="whitegrid")

import ktool

# %%time