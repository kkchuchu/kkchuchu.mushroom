import sys

import pandas as pd
import seaborn as sns


COLORS = ['black', 'blue', 'purple', 'yellow', 'white', 'red', 'lime', 'cyan', 'orange', 'gray']

def create_notebook_env():
    # pd.set_option('display.expand_frame_repr', False)
    sns.set(style="whitegrid", color_codes=True)
    pd.options.display.max_columns = None


def check_df_before_modeling(df):
    is_null_count = d.isnull().sum()
    print('is null check result:')
    print(is_null_count)
