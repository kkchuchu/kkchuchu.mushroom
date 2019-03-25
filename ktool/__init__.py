import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
from scipy.stats import norm, skew
import seaborn as sns

def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn
# pd.set_option('display.expand_frame_repr', False)
sns.set(style="whitegrid", color_codes=True)
