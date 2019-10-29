#!/usr/bin/python3

import sys



COLORS = ['black', 'blue', 'purple', 'yellow', 'white', 'red', 'lime', 'cyan', 'orange', 'gray']

def create_notebook_env():
    import seaborn as sns
    import pandas as pd
    # pd.set_option('display.expand_frame_repr', False)
    sns.set(style="whitegrid", color_codes=True)
    pd.options.display.max_columns = None


def check_df_before_modeling(df):
    is_null_count = d.isnull().sum()
    print('is null check result:')
    print(is_null_count)

def get_basic(df):
    print("=======")
    print(df.info())
    print("=======")
    print(df.isnull().sum())
    print("=======")
    df.head()

def xgb_plot_features(booster, figsize=(10,14)):
    from xgboost import plot_importance
    fig, ax = plt.subplots(1,1,figsize=figsize)
    return plot_importance(booster=booster, ax=ax)


def boxplot(df, column):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,4))
    plt.xlim(df[[column]].min(), df[['column']].max()*1.1)
    sns.boxplot(x=df[[column]])


def inorder_traversal(node, get_value_m, r):
    if node is None:
        return

    inorder_traversal(node.left, get_value_m, r)
    r.append(get_value_m(node))
    inorder_traversal(node.right, get_value_m, r)


def bfs_bst(node):
    queue = [node]
    r = []
    while len(queue) > 0:
        cursor = queue.pop(0)
        if cursor:
            r.append(cursor.val)
        else:
            r.append(None)
            continue
        if cursor.left:
            queue.append(cursor.left)
        else:
            queue.append(None)
        if cursor.right:
            queue.append(cursor.right)
        else:
            queue.append(None)
    return r

def to_time_flow(df: pd.DataFrame, 
                 time_column:str, flow_target_column:str, count_column:str =None, 
                 time_range:list =None, default_value=0.):
    """Convert a dataframe into a new dataframe with time index.

    Parameters
    ----------
    df : 
        data frame contains time data.
    time_column :
        time column.

    Returns
    -------
    DataFrame
        data frame with time index.

    """
    group_key = [time_column, flow_target_column]
    if count_column is None:
        t = df.groupby(by=group_key).size().reset_index(name='count')
    else:
        t = df.groupby(by=group_key)[count_column].sum().reset_index(name='count')
    
    trend = t.pivot(index=time_column, columns=flow_target_column, values='count') \
             .fillna(default_value)
    if time_range is not None:
        trend = trend.reindex(pd.date_range(time_range[0], time_range[1]), fill_value=default_value)
    return trend
