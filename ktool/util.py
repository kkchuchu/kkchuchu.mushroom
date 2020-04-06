import socket
import struct
import datetime
from pathlib import Path
from configparser import ConfigParser
import os
import json
import os
import datetime
import time
import pytz
import dateutil

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
        ts = (t - np.datetime64('1970-01-01T00:00:00Z')) / \
            np.timedelta64(1, 's')
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


def time_converter(t, return_type="dt", timezone=pytz.utc, time_format="%Y-%m-%d"):
    if return_type == "ts":
        return datetime.datetime.timestamp(t)
    elif return_type == "dt":
        if isinstance(t, (int, float)):
            return datetime.datetime.utcfromtimestamp(t).replace(tzinfo=pytz.utc)
        elif isinstance(t, (datetime.datetime)):
            return t.replace(tzinfo=timezone)
        elif isinstance(t, (str)):
            try:
                return dateutil.parser.parse(t) # example: '2020-04-05T20:00:00.000Z', rfc822
            except ValueError:
                return datetime.datetime.strptime(t, format=time_format)

def to_time_flow(df: pd.DataFrame,
                 group_by_col: list, agg: dict,
                 time_range_start=None, time_range_end=None, time_range_freq="1S"):
    if time_range_start is None:
        time_range_start = df[group_by_col].min()[0]
    if time_range_end is None:
        time_range_end = df[group_by_col].max()[0]
    new_ix = pd.date_range(
        time_range_start, time_range_end, freq=time_range_freq)
    trend = df.groupby(group_by_col).agg(agg).reindex(new_ix, fill_value=0.)

    return trend


def display_tree(a_tree):
    import graphviz
    from sklearn.tree import export_graphviz

    dot_data = export_graphviz(a_tree, out_file=None)
    graph = graphviz.Source(dot_data)
    return graph


class BaseConfig(object):

    def __init__(self, root_path, project_name, created_time: datetime.datetime = None, created_time_format="ts"):
        """[summary]
        {root}/{project}/{time}/
        Arguments:
            log_base_folder_path {[type]} -- [description]
            project_name {[type]} -- [description]

        Keyword Arguments:
            created_time {datetime.datetime} -- [description] (default: {None})
            created_time_format {str} -- [description] (default: {"ts"})
        """
        self._root_path = os.path.abspath(root_path)
        self._project_name = project_name
        self._created_time_format = created_time_format
        self._tmp_folder_word = "_tmp"
        if created_time is None:
            self._created_time = datetime.datetime.now()
        else:
            self._created_time = created_time
        self._created_time_str = "{created_time}".format(
            created_time=self._get_created_time_str())

    def _get_created_time_str(self):
        if self._created_time_format == "ts":
            import calendar
            ts = calendar.timegm(self._created_time.timetuple())
            return str(ts)
        else:
            return self._created_time.strftime(self._created_time_format)

    def get_project_folder(self):
        return os.path.join(self._root_path, self._project_name)

    def get_this_time_project_folder(self):
        path = os.path.join(
            self._root_path, self._project_name, self._created_time_str)
        self._create_folder_without_error(path)
        return path

    def get_project_tmp_folder(self):
        """[summary]
        tmp folder should not keep for a long time.    
        Returns:
            [str] -- [tmp folder path]
        """
        this_time_project_folder = self.get_this_time_project_folder()
        path = os.path.join(this_time_project_folder, self._tmp_folder_word)

        self._create_folder_without_error(path)
        return path

    def _create_folder_without_error(self, full_file_path):
        folder_path = os.path.dirname(full_file_path)
        Path(folder_path).mkdir(exist_ok=True,  parents=True)

    def _get_folder_file_with_latest_n_files_ordered_by_changed_time(self, n, folder_path):
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                 if os.path.isfile(os.path.join(folder_path, f))]

        files = sorted([f for f in files],
                       key=lambda f: os.path.getmtime(f), reverse=True)[:n]
        return files
