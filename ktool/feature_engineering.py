import pandas as pd
import seaborn as sns
from IPython.display import display, HTML
from matplotlib import pyplot as plt


def run(df: pd.DataFrame, hue: str=None, columns: list=None, display=display, category_columns: list=None, y_column=None):
    if columns is None:
        columns = df.columns

    display(df.head())
    display(df.describe())
    print('records count are: ', len(df))

    print('duplicated: ', df.duplicated().sum())

    target_df = df[columns]
    if hue is None:
        r = sns.pairplot(target_df)
    else:
        r = sns.pairplot(target_df, hue=hue)
    display(r)

    for cat_col in category_columns:
        display(barplot(x=cat_col, y=y_column, data=df))
        
    heatmap(df)


def cat2cat(df: pd.DataFrame, x, y, hue: str=None):
    sns.catplot(x, y, hue=hue, data=df)


def cont2cont(df: pd.DataFrame, x, y, hue: str=None):
    '''
    Doc: https://seaborn.pydata.org/generated/seaborn.relplot.html
    '''
    sns.relplot(df, x, y, hue=hue, data=df)


def top(df, column: str, n: int=5):
    display(df.sort_values(column, ascending=False).head(n))


def cat2count(df, x: str):
    sns.countplot(x=x, data=df)


def heatmap(df):
    sns.heatmap(df.corr())

from enum import Enum
class BarType(Enum):
    DEFAULT = 1
    HOLLOW  = 2


def barplot(x=None, y=None, data=None, xlabel=None, ylabel=None, bar_type=BarType.DEFAULT):
    plt.figure(figsize=(8, 8))
    plt.xticks(rotation=90)
    ax = _decide_bar_type(x, y, data, bar_type) 
    if xlabel is None or ylabel is None:
        ax.set(xlabel=xlabel, ylabel=ylabel)
    return ax

def _decide_bar_type(x, y, data, type_):
    if type_ == BarType.DEFAULT:
        return sns.barplot(x=x, y=y, data=data)
    elif type_ == BarType.HOLLOW:
        return sns.barplot(x=x, y=y, data=data,
                     linewidth=2.5, facecolor=(1, 1, 1, 0),
                     errcolor=".2", edgecolor=".2")



def sort(df, by=None):
    return df.sort_values(by=by, ascending=False)


def get_top_what1_of_what2(df, what1: str, what2: str, top=6):
    return df.groupby(by=[what1])[what2] \
        .sum() \
        .reset_index() \
        .sort_values(by=[what2], ascending=False).head(top)[what1].values
