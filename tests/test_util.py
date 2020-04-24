import sys
import json
import unittest
import os
import datetime
from unittest.mock import patch
from joblib import dump, load
import numpy as np
import shutil
import pytz
import random

import pandas as pd

from ktool.util import TS, IP, to_flow


class TestKToolUtil(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        cls.seed = 10

    @classmethod
    def teardown_class(cls):
        """Run only once in the testcases
        """
        try:
            # folder_path = cls.config._get_log_base_folder()
            # shutil.rmtree(folder_path, ignore_errors=True)
            pass
        except FileNotFoundError as e:
            pass

    def tearDown(self):
        pass

    def setUp(self):
        random.seed(self.seed)
        self.df = pd.DataFrame()
        index = pd.date_range('1/1/2000', periods=9, freq='T')
        self.ds = pd.Series(range(9), index=index)

    def test_time_converter__normal(self):
        e_d = datetime.datetime(
            year=2020, month=4, day=5, hour=10, tzinfo=pytz.utc)
        e_t = e_d.timestamp()

        for t in ["2020-04-05T10:00:00.000Z",
                  datetime.datetime(year=2020, month=4, day=5, hour=10, tzinfo=pytz.utc), 
                  datetime.datetime.strptime("20200405100000", "%Y%m%d%H%M%S"),
                  pytz.timezone('Asia/Shanghai').localize(datetime.datetime.strptime("20200405180000", "%Y%m%d%H%M%S")),
                  ]:
            d = TS.to(t, to_type=TS.DATETIME)
            t = TS.to(t, to_type=TS.TIMESTAMP)

            self.assertEqual(e_d, d)
            self.assertEqual(e_t, t)

    def test_time_converter__ts_tz_is_str(self):
        e_d = datetime.datetime(
            year=2020, month=4, day=5, hour=10, tzinfo=pytz.utc)
        e_t = e_d.timestamp()

        t = datetime.datetime(year=2020, month=4, day=5, hour=18)
        d = TS.to(t, ts_tz="Asia/Taipei", to_type=TS.DATETIME)
        t = TS.to(t, ts_tz="Asia/Taipei", to_type=TS.TIMESTAMP)

        self.assertEqual(e_d, d)
        self.assertEqual(e_t, t)
            
    def test_ip_converter__normal(self):
        self.assertEqual(IP.to(0xc0a80164), '192.168.1.100')
        self.assertEqual(IP.to('10.0.0.1'), 167772161)
        self.assertEqual(IP.to(167772161), '10.0.0.1')

    def test_to_flow__normal(self):
        flow_df = to_flow(self.ds, resample_freq="1H",
                          resample_agg=["max", "count"])
