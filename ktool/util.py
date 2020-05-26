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
    def to(t, to_type=DATETIME, ts_tz=pytz.utc, format=None, *args, **kwargs):
        """[summary]

        Arguments:
            t {[type]} -- [description]

        Keyword Arguments:
            to_type {[type]} -- [description] (default: {DATETIME})
            ts_tz {str, pytz.utc like} -- Support str and pytz.utc like object (default: {pytz.utc})
            time_format {str} -- [description] (default: {"%Y-%m-%d"})

        Raises:
            NotSupportedError: [description]

        Returns:
            [datetime] -- depends on to_type with utc timezone
        """
        
        # convert timezone
        if isinstance(ts_tz, (str)):
            ts_tz = pytz.timezone(ts_tz)
            
        r = pd.to_datetime(t, format=format, **kwargs)
        if r.tzinfo is None:
            r = r.tz_localize(ts_tz)
        else:
            r = r.astimezone(ts_tz)
            
            
        if to_type == TS.DATETIME:
            pass
        elif to_type == TS.TIMESTAMP:
            r = datetime.datetime.timestamp(r)
        else:
            raise NotSupportedError()
        return r

    @staticmethod
    def _replace_tz(t, ts_tz):
        if t.tzinfo is None: # set timezone
            t = ts_tz.localize(t)
        if t.tzinfo != pytz.utc: # convert timezone
            t = t.astimezone(pytz.utc)
        return t


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


def to_flow(df: (pd.DataFrame, pd.Series),
            group_by_col: str=None, deduplicate_agg: dict=None,
            resample_freq="1T", resample_agg: list=None,
            timezone = "UTC"
            ):
    """
    Ref: https://pandas.pydata.org/docs/user_guide/timeseries.html

    Args:
        df ([type]): [description]
        group_by_col (str, optional): [description]. Defaults to None.
        deduplicate_agg (dict, optional): [description]. Defaults to None.
        resample_freq (str, optional): [description]. Defaults to "1T".
        resample_agg (list, optional): [description]. Defaults to None.
        timezone (str, optional): [description]. Defaults to "UTC".

    Raises:
        NotSupportedError: [description]

    Returns:
        [type]: [description]
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
    t1 = t1.tz_localize(timezone)
    t1['_date'] = pd.to_datetime(t1.index, utc = True)
    return t1


def display_tree(a_tree):
    import graphviz
    from sklearn.tree import export_graphviz

    dot_data = export_graphviz(a_tree, out_file=None)
    graph = graphviz.Source(dot_data)
    return graph
