import socket
import struct
import datetime
from pathlib import Path
from configparser import ConfigParser
import os

import pandas as pd
import numpy as np
from sklearn.tree import _tree

from pyspark import SparkConf


def set_spark_conf(spark_master_url, app_name, spark_serializer, spark_jars):
    sc_conf = SparkConf() \
            .setMaster(spark_master_url) \
            .setAppName(app_name) \
            .set("spark.serializer", spark_serializer) \
            .set("spark.jars", spark_jars)
    return sc_conf

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


class TimeConverter(object):
    
    @staticmethod
    def toTS(t):
        if isinstance(t, datetime.datetime):
            return TimeConverter.datetime2timestamp(t)
        else:
            return TimeConverter.iso8601toseconds(t)
        
    @staticmethod
    def toDT(t):
        if isinstance(t, (float, int)):
            return TimeConverter.timestamp2datetime(t)
        elif isinstance(t, np.datetime64):
            return TimeConverter.numpydatetime2timestamp(t)
        else:
            return TimeConverter.str2datetime(t)
            
    @staticmethod
    def iso8601toseconds(t):
        import dateutil.parser as dp
        parsed_t = dp.parse(t)
        t_in_seconds = parsed_t.strftime('%s')
        return t_in_seconds

    @staticmethod
    def datetime2timestamp(t):
        return int(t.timestamp())

    @staticmethod
    def timestamp2datetime(t):
        return datetime.datetime.fromtimestamp(t)

    @staticmethod
    def str2datetime(t):
        return pd.to_datetime(t)

    @staticmethod
    def numpydatetime2timestamp(t: np.datetime64):
        ts = (t - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        return ts


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
                 time_range:list =None, default_value=0.,
                 time_str_format = '%Y%m%d%H%M%S',
                 agg_freq="1S"):
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
            
    df["_datetime_column"] = df.apply(lambda x: TimeConverter.toDT(x), axis=1)

    group_key = ["_datetime_column", flow_target_column]
    if count_column is None: # count records
        t = df.groupby(by=group_key).size().reset_index(name='count')
    else: # sum records
        t = df.groupby(by=group_key)[count_column].sum().reset_index(name='count')
    
    # trend = t.pivot(index=time_column, columns=flow_target_column, values='count') \
    #          .fillna(default_value)
    if time_range is not None:
        time_range = pd.date_range(time_range[0], time_range[1], freq=agg_freq)
    else:
        time_range = pd.date_range(df.index.min(), df.index.max(), freq=agg_freq)
    trend = trend.reindex(time_range, fill_value=default_value)
    return trend


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


class BaseConfig(object):
    
    def __init__(self, log_base_folder_path, project_name, created_time:datetime.datetime=None, created_time_format="ts"):
        self._log_base_folder_path = log_base_folder_path
        self._project_name = project_name
        self._created_time_format = created_time_format
        self._tmp_folder_word = "tmp"
        if created_time is None:
            self._created_time = datetime.datetime.now()
        else:
            self._created_time = created_time
            
            
    def _get_created_time_str(self):
        if self._created_time_format == "ts":
            import calendar
            ts = calendar.timegm(self._created_time.timetuple())
            return str(ts)
        else:
            return self._created_time.strftime(self._created_time_format)
        
    def _get_log_base_folder(self):
        file_path = self._log_base_folder_path
        return os.path.abspath(file_path)
    
    def get_project_base_folder(self):
        root_folder = self._get_log_base_folder()
        project_time_folder = os.path.join(root_folder, self._project_name, "{created_time}")
        project_folder = project_time_folder.format(created_time=self._get_created_time_str())
        path = os.path.join(root_folder, project_folder)
        self._create_folder_without_error(path)
        return path
    
    def get_project_tmp_folder(self):
        """[summary]
        tmp folder should not keep for a long time.    
        Returns:
            [str] -- [tmp folder path]
        """
        root_folder = self._get_log_base_folder()
        path = os.path.join(root_folder, self._tmp_folder_word + "_" + self._project_name)
        
        self._create_folder_without_error(path)
        return path
    
    def get_project_file_path(self, config_field_name):
        base_folder = self.get_project_base_folder()
        file_path = self._config.get(self._project_name, config_field_name)
        path = os.path.join(base_folder, file_path)
        self._create_folder_without_error(path)
        return path
        
    def _create_folder_without_error(self, full_file_path):
        folder_path = os.path.dirname(full_file_path)
        Path(folder_path).mkdir(exist_ok=True,  parents=True)
    
    def _get_folder_file_with_latest_n_files_ordered_by_changed_time(self, n, folder_path):
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
                 if os.path.isfile(os.path.join(folder_path, f))]
        
        files = sorted([f for f in files], key=lambda f: os.path.getmtime(f), reverse=True)[:n]
        return files