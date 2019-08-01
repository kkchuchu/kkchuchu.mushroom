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
