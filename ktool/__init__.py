import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
from scipy import stats
import seaborn as sns


def create_notebook_env():
    def ignore_warn(*args, **kwargs):
        pass
    warnings.warn = ignore_warn
    # pd.set_option('display.expand_frame_repr', False)
    sns.set(style="whitegrid", color_codes=True)
    pd.options.display.max_columns = None
