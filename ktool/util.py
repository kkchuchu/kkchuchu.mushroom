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


class IP(object):

    @staticmethod
    def to(t):
        # TODO: ipv6
        if type(t) in IPType2Method:
            return IPType2Method[type(t)](t)
        else:
            raise NotSupportedError()

    @staticmethod
    def _ip2int(addr):
        return struct.unpack("!I", socket.inet_aton(addr))[0]

    @staticmethod
    def _int2ip(addr):
        return socket.inet_ntoa(struct.pack("!I", addr))


IPType2Method = {
    (str): IP._ip2int,
    (int): IP._int2ip
}


class TS(object):
    DATETIME = 1
    TIMESTAMP = 2

    @staticmethod
    def to(t, to_type=DATETIME, tz=pytz.utc, time_format="%Y-%m-%d"):
        r = None
        if type(t) in TSType2Method:
            r = TSType2Method[type(t)](t, tz, time_format)
        else:
            raise NotSupportedError()

        if to_type == TS.DATETIME:
            return r
        elif to_type == TS.TIMESTAMP:
            return datetime.datetime.timestamp(r)
        else:
            raise NotSupportedError()

    @staticmethod
    def _replace_tz(t, tz, time_format):
        return t.replace(tzinfo=tz)

    @staticmethod
    def _int_to_datetime(t, tz, time_format):
        return datetime.datetime.utcfromtimestamp(
            t).replace(tzinfo=pytz.utc)

    @staticmethod
    def _np64_to_datetime(t, tz, time_format):
        ts = (t - np.datetime64('1970-01-01T00:00:00Z')) / \
            np.timedelta64(1, 's')
        r = datetime.datetime.utcfromtimestamp(
            ts).replace(tzinfo=pytz.utc)

        return r

    @staticmethod
    def _str_to_datetime(t, tz, time_format):
        try:
            # example: '2020-04-05T20:00:00.000Z', rfc822, iso8601
            r = dateutil.parser.parse(t)
        except ValueError:
            r = datetime.datetime.strptime(
                t, format=time_format).replace(tzinfo=tz)

        return r


TSType2Method = {
    (datetime.datetime): TS._replace_tz,
    (float, int): TS._int_to_datetime,
    (np.datetime64): TS._np64_to_datetime,
    (str): TS._str_to_datetime
}


class NotSupportedError(Exception):
    pass


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
                 group_by_col: list, agg: dict,
                 time_range_start=None, time_range_end=None, time_range_freq="1S"):
    """
    util.to_time_flow(alert_df,
                 group_by_col=['key_as_string'],
                 agg={'doc_count': 'max'}, time_range_freq='1H')
    """
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
