import socket
import struct

import pandas as pd
from sklearn.tree import _tree


def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


def iso8601toseconds(t):
    import dateutil.parser as dp
    parsed_t = dp.parse(t)
    t_in_seconds = parsed_t.strftime('%s')
    return t_in_seconds


def datetimetotimestamp(t):
    return int(t.timestamp())


def strtodatetime(t):
    return pd.to_datetime(t)


def count_by(df: pd.DataFrame, by: list = []):
    """
    Counting by the key list.
    
    Arguments:
        df {pd.DataFrame} -- data source
    
    Keyword Arguments:
        by {list} -- key list (default: {[]})
    
    Returns:
        [pd.DataFrame] -- group by result
    """
    r = df.groupby(by=by).size().reset_index(name='count')
    for x in by:
        r.plot(x=x, y='count')
    return r

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def to_time_flow(df: pd.DataFrame, 
                 time_column:str, flow_target_column:str, count_column:str =None, 
                 time_range:list =None, default_value=0.):
    """Convert a dataframe into a new dataframe with time index.
    date_range freq: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases

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
    return tren


def tree_to_code(tree, feature_names):
    """
    Outputing decision tree rules.
    https://stackoverflow.com/questions/20224526/how-to-extract-the-decision-rules-from-scikit-learn-decision-tree
    """
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    print("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print("{}if {} <= {}:".format(indent, name, threshold))
            recurse(tree_.children_left[node], depth + 1)
            print("{}else:  # if {} > {}".format(indent, name, threshold))
            recurse(tree_.children_right[node], depth + 1)
        else:
            print("{}return {}".format(indent, tree_.value[node]))

    recurse(0, 1)
