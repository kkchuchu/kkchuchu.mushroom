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


def set_spark_conf(spark_master_url, app_name, spark_serializer, spark_jars):
    from pyspark import SparkConf
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
        for type_, method in IPType2Method.items():
            if isinstance(t, type_):
                return method(t)
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
    def to(t, to_type=DATETIME, ts_tz=pytz.utc, time_format="%Y-%m-%d"):
        """[summary]

        Arguments:
            t {[type]} -- [description]

        Keyword Arguments:
            to_type {[type]} -- [description] (default: {DATETIME})
            ts_tz {[type]} -- [description] (default: {pytz.utc})
            time_format {str} -- [description] (default: {"%Y-%m-%d"})

        Raises:
            NotSupportedError: [description]

        Returns:
            [datetime] -- depends on to_type with utc timezone
        """
        if isinstance(ts_tz, (str)):
            ts_tz = pytz.timezone(ts_tz)
            
        r = None
        for type_, method in TSType2Method.items():
            if isinstance(t, type_):
                r = method(t, ts_tz, time_format)
                break
        else:
            raise NotSupportedError()

        if to_type == TS.DATETIME:
            return r
        elif to_type == TS.TIMESTAMP:
            return datetime.datetime.timestamp(r)
        else:
            raise NotSupportedError()

    @staticmethod
    def _replace_tz(t, ts_tz, time_format):
        if t.tzinfo is None:
            t = ts_tz.localize(t)
        if t.tzinfo != pytz.utc:
            t = t.astimezone(pytz.utc)
        return t

    @staticmethod
    def _int_to_datetime(t, tz, time_format):
        return datetime.datetime.utcfromtimestamp(
            t).replace(tzinfo=tz)

    @staticmethod
    def _np64_to_datetime(t, tz, time_format):
        ts = (t - np.datetime64('1970-01-01T00:00:00Z')) / \
            np.timedelta64(1, 's')
        r = datetime.datetime.utcfromtimestamp(
            ts).replace(tzinfo=tz)

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


def to_flow(df: (pd.DataFrame, pd.Series),
            group_by_col: str=None, deduplicate_agg: dict=None,
            resample_freq="1T", resample_agg: list=None,
            timezone = "UTC"
            ):
    """
    Ref: https://pandas.pydata.org/docs/user_guide/timeseries.html
    
    Arguments:
        df {pd.DataFrame} -- [description]
        group_by_col {str} -- [description]
        deduplicate_agg {dict} -- [description]
    
    Keyword Arguments:
        resample_freq {str} -- [description] (default: {"1T"})
        resample_agg {list} -- [description] (default: {None})
    
    Returns:
        [type] -- [description]
    """
    if isinstance(df, (pd.DataFrame)):
        t1 = df.groupby(group_by_col).agg(deduplicate_agg) # deduplicate
        flow_field = list(deduplicate_agg.keys())[0]
        t1 = pd.Series(t1[flow_field].values, index=t1.index.values)
    elif isinstance(df, (pd.Series)):
        t1 = df
    else:
        raise NotSupportedError()
    if "count" not in resample_agg:
        resample_agg.append("count")
    t1 = t1.resample(resample_freq).aggregate(resample_agg)
    t1.tz_localize(timezone)
    return t1


def display_tree(a_tree):
    import graphviz
    from sklearn.tree import export_graphviz

    dot_data = export_graphviz(a_tree, out_file=None)
    graph = graphviz.Source(dot_data)
    return graph
