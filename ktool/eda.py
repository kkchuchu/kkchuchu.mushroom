from datetime import datetime

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype, is_categorical_dtype


def run(df: pd.DataFrame, columns: list=None, category_columns: list=[], datetime_columns: list=[], numeric_columns: list=[],
        string_columns: list=[],
        drop_duplicated=False,
        display_heatmap=False, display_duplicated=True, 
        height=DEFAULT_IMAGE_HEIGHT, display=display, color_map=DEFAULT_COLOR_MAP, 
       ):
    if columns is None:
        columns = df.columns

        
    # basic information
    display(df.head())
    display(df.describe())
    print('records count are: ', len(df))
    
    duplicated_count = df.duplicated(subset=columns).sum()
    print('duplicated: ', duplicated_count)
    if display_duplicated and duplicated_count > 0:
        display(df[df.duplicated(subset=columns)])
    
    
    print('null check: ')
    print(df.isnull().sum())
    # TODO fill null
    
    
    # drop duplicate and reset index
    if drop_duplicated:
        # TODO
        assert False

        
    # type convert
    for cat_col in category_columns:
        df[cat_col] = df[cat_col].astype('category')
        
    for col in datetime_columns:
        if is_numeric_dtype(df.dtypes[col]):
            df[col] = df.apply(lambda x: datetime.fromtimestamp(x[col]), axis=1)
        else:
            df[col] = pd.to_datetime(df[col])
            
    for col in string_columns:
        df[col] = df[col].astype('unicode')
    

    # heatmap
    if display_heatmap:
        plt.figure()
        sns.heatmap(df.corr(), annot=True, cmap=color_map)