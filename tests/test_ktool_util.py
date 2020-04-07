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

from ktool.util import TS, IP


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

    def test_time_converter__normal(self):
        e_d = datetime.datetime(
            year=2020, month=4, day=5, hour=10, tzinfo=pytz.utc)
        e_t = e_d.timestamp()

        for t in ["2020-04-05T10:00:00.000Z",
                  datetime.datetime(year=2020, month=4, day=5, hour=10, tzinfo=pytz.utc)]:
            d = TS.to(t, to_type=TS.DATETIME)
            t = TS.to(t, to_type=TS.TIMESTAMP)

            self.assertEqual(e_d, d)
            self.assertEqual(e_t, t)

    def test_ip_converter__normal(self):
        self.assertEqual(IP.to(0xc0a80164), '192.168.1.100')
        self.assertEqual(IP.to('10.0.0.1'), 167772161)
        self.assertEqual(IP.to(167772161), '10.0.0.1')
